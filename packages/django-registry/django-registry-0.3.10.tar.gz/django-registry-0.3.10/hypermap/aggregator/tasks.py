from __future__ import absolute_import

import logging
from celery import chain
from django.conf import settings
from django.core.cache import cache

from celery import shared_task

LOGGER = logging.getLogger(__name__)

REGISTRY_LIMIT_LAYERS = getattr(settings, 'REGISTRY_LIMIT_LAYERS', -1)
REGISTRY_SEARCH_URL = getattr(settings, 'REGISTRY_SEARCH_URL', None)

if REGISTRY_SEARCH_URL is None:
    SEARCH_ENABLED = False
    SEARCH_TYPE = None
    SEARCH_URL = None
else:
    SEARCH_ENABLED = True
    SEARCH_TYPE = REGISTRY_SEARCH_URL.split('+')[0]
    SEARCH_URL = REGISTRY_SEARCH_URL.split('+')[1]


if REGISTRY_LIMIT_LAYERS > 0:
    DEBUG_SERVICES = True
    DEBUG_LAYERS_NUMBER = REGISTRY_LIMIT_LAYERS
else:
    DEBUG_SERVICES = False
    DEBUG_LAYERS_NUMBER = -1


@shared_task(bind=True)
def check_all_services(self):
    from hypermap.aggregator.models import Service
    service_to_processes = Service.objects.filter(active=True)
    total = service_to_processes.count()
    count = 0
    for service in service_to_processes:
        # update state
        if not self.request.called_directly:
            self.update_state(
                state='PROGRESS',
                meta={'current': count, 'total': total}
            )
        check_service.delay(service)
        count = count + 1


@shared_task(bind=True)
def check_service(self, service):
    # total is determined (and updated) exactly after service.update_layers
    total = 100

    def status_update(count):
        if not self.request.called_directly:
            self.update_state(
                state='PROGRESS',
                meta={'current': count, 'total': total}
            )

    status_update(0)

    if getattr(settings, 'REGISTRY_HARVEST_SERVICES', True):
        service.update_layers()
        service.index_layers()
    # we count 1 for update_layers and 1 for service check for simplicity
    layer_to_process = service.layer_set.all()

    if DEBUG_SERVICES:
        layer_to_process = layer_to_process[0:DEBUG_LAYERS_NUMBER]

    total = layer_to_process.count() + 2
    status_update(1)
    service.check_available()
    status_update(2)
    count = 3

    if not settings.REGISTRY_SKIP_CELERY:
        tasks = []
        for layer in layer_to_process:
            # update state
            status_update(count)
            # send subtasks to make a non-parallel execution.
            tasks.append(check_layer.si(layer))
            count += 1
        # non-parallel execution will be performed in chunks of 100 tasks
        # to avoid run time errors with big chains.
        size = 100
        chunks = [tasks[i:i + size] for i in range(0, len(tasks), size)]
        for chunk in chunks:
            chain(chunk)()
    else:
        for layer in layer_to_process:
            status_update(count)
            check_layer(layer)
            count += 1


@shared_task(bind=True, time_limit=10)
def check_layer(self, layer):
    LOGGER.debug('Checking layer %s' % layer.name)
    success, message = layer.check_available()
    # every time a layer is checked it should be indexed
    # for now we remove indexing but we do it using a scheduled task unless SKIP_CELERY_TASK
    if success and SEARCH_ENABLED:
        if settings.REGISTRY_SKIP_CELERY:
            index_layer(layer)
        else:
            # we cache the layer id
            LOGGER.debug('Caching layer with id %s for syncing with search engine' % layer.id)
            layers = cache.get('layers')
            if layers is None:
                layers = set([layer.id,])
            else:
                layers.add(layer.id)
            cache.set('layers', layers)
    if not success:
        from hypermap.aggregator.models import TaskError
        task_error = TaskError(
            task_name=self.name,
            args=layer.id,
            message=message
        )
        task_error.save()


@shared_task(bind=True)
def index_cached_layers(self):
    """
    Index all layers in the Django cache (Index all layers who have been checked).
    """
    from hypermap.aggregator.models import Layer
    from hypermap.aggregator.models import TaskError

    if SEARCH_TYPE == 'solr':
        from hypermap.aggregator.solr import SolrHypermap
        solrobject = SolrHypermap()
    else:
        from hypermap.aggregator.elasticsearch_client import ESHypermap
        from elasticsearch import helpers
        es_client = ESHypermap()

    layers_cache = cache.get('layers')

    if layers_cache:
        layers_list = list(layers_cache)
        LOGGER.debug('There are %s layers in cache: %s' % (len(layers_list), layers_list))

        batch_size = settings.REGISTRY_SEARCH_BATCH_SIZE
        batch_lists = [layers_list[i:i+batch_size] for i in range(0, len(layers_list), batch_size)]

        for batch_list_ids in batch_lists:
            layers = Layer.objects.filter(id__in=batch_list_ids)

            if batch_size > len(layers):
                batch_size = len(layers)

            LOGGER.debug('Syncing %s/%s layers to %s: %s' % (batch_size, len(layers_cache), layers, SEARCH_TYPE))

            try:
                if SEARCH_TYPE == 'solr':
                    success, message = solrobject.layers_to_solr(layers)
                elif SEARCH_TYPE == 'elasticsearch':
                    with_bulk, success = True, False
                    layers_to_index = [es_client.layer_to_es(layer, with_bulk) for layer in layers]
                    message = helpers.bulk(es_client.es, layers_to_index)

                    # Check that all layers where indexed...if not, don't clear cache.
                    # TODO: Check why es does not index all layers at first.
                    len_indexed_layers = message[0]
                    if len_indexed_layers == len(layers):
                        LOGGER.debug('%d layers indexed successfully' % (len_indexed_layers))
                        success = True
                else:
                    raise Exception("Incorrect SEARCH_TYPE=%s" % SEARCH_TYPE)
                if success:
                    # remove layers from cache here
                    layers_cache = layers_cache.difference(set(batch_list_ids))
                    cache.set('layers', layers_cache)
                else:
                    task_error = TaskError(
                        task_name=self.name,
                        args=batch_list_ids,
                        message=message
                    )
                    task_error.save()
            except Exception as e:
                LOGGER.error('Layers were NOT indexed correctly')
                LOGGER.error(e, exc_info=True)
    else:
        LOGGER.debug('No cached layers.')


@shared_task(name="clear_index")
def clear_index():
    if SEARCH_TYPE == 'solr':
        LOGGER.debug('Clearing the solr core and indexes')
        from hypermap.aggregator.solr import SolrHypermap
        solrobject = SolrHypermap()
        solrobject.clear_solr()
    elif SEARCH_TYPE == 'elasticsearch':
        LOGGER.debug('Clearing the ES indexes')
        from hypermap.aggregator.elasticsearch_client import ESHypermap
        esobject = ESHypermap()
        esobject.clear_es()


@shared_task(bind=True)
def remove_service_checks(self, service):

    service.check_set.all().delete()

    def status_update(count, total):
        if not self.request.called_directly:
            self.update_state(
                state='PROGRESS',
                meta={'current': count, 'total': total}
            )

    layer_to_process = service.layer_set.all()
    count = 0
    total = layer_to_process.count()
    for layer in layer_to_process:
        # update state
        status_update(count, total)
        layer.check_set.all().delete()
        count = count + 1


@shared_task(bind=True)
def index_service(self, service):

    layer_to_process = service.layer_set.all()
    total = layer_to_process.count()

    def status_update(count):
        if not self.request.called_directly:
            self.update_state(
                state='PROGRESS',
                meta={'current': count, 'total': total}
            )

    count = 0
    for layer in layer_to_process:
        # update state
        status_update(count)
        if not settings.REGISTRY_SKIP_CELERY:
            index_layer.delay(layer)
        else:
            index_layer(layer)
        count = count + 1


@shared_task(bind=True)
def index_layer(self, layer):
    # TODO: Make this function more DRY
    # by abstracting the common bits.
    if SEARCH_TYPE == 'solr':
        from hypermap.aggregator.solr import SolrHypermap
        LOGGER.debug('Syncing layer %s to solr' % layer.name)
        try:
            solrobject = SolrHypermap()
            success, message = solrobject.layer_to_solr(layer)
            if not success:
                from hypermap.aggregator.models import TaskError
                task_error = TaskError(
                    task_name=self.name,
                    args=layer.id,
                    message=message
                )
                task_error.save()
        except Exception, e:
            LOGGER.error('Layers NOT indexed correctly')
            LOGGER.error(e, exc_info=True)
            self.retry(layer)
    elif SEARCH_TYPE == 'elasticsearch':
        from hypermap.aggregator.elasticsearch_client import ESHypermap
        LOGGER.debug('Syncing layer %s to es' % layer.name)
        esobject = ESHypermap()
        success, message = esobject.layer_to_es(layer)
        if not success:
            from hypermap.aggregator.models import TaskError
            task_error = TaskError(
                task_name=self.name,
                args=layer.id,
                message=message
            )
            task_error.save()


@shared_task(bind=True)
def index_all_layers(self):
    from hypermap.aggregator.models import Layer

    layer_to_processes = Layer.objects.all()
    total = layer_to_processes.count()
    count = 0
    for layer in Layer.objects.all():
        # update state
        if not self.request.called_directly:
            self.update_state(
                state='PROGRESS',
                meta={'current': count, 'total': total}
            )
        if not settings.REGISTRY_SKIP_CELERY:
            index_layer.delay(layer)
        else:
            index_layer(layer)
        count = count + 1


@shared_task(bind=True)
def update_endpoint(self, endpoint, greedy_opt=False):
    from hypermap.aggregator.utils import create_services_from_endpoint
    from hypermap.aggregator.models import Endpoint

    LOGGER.debug('Processing endpoint with id %s: %s' % (endpoint.id, endpoint.url))

    # Override the greedy_opt var with the value from the endpoint list
    # if it's available.
    if endpoint.endpoint_list:
        greedy_opt = endpoint.endpoint_list.greedy

    imported, message = create_services_from_endpoint(endpoint.url, greedy_opt=greedy_opt, catalog=endpoint.catalog)

    # this update will not execute the endpoint_post_save signal.
    Endpoint.objects.filter(id=endpoint.id).update(
        imported=imported, message=message, processed=True
    )


@shared_task(bind=True)
def update_endpoints(self, endpoint_list):
    # for now we process the enpoint even if they were already processed
    endpoint_to_process = endpoint_list.endpoint_set.filter(processed=False)
    total = endpoint_to_process.count()
    count = 0
    if not settings.REGISTRY_SKIP_CELERY:
        for endpoint in endpoint_to_process:
            update_endpoint.delay(endpoint)
        # update state
        if not self.request.called_directly:
            self.update_state(
                state='PROGRESS',
                meta={'current': count, 'total': total}
            )
    else:
        for endpoint in endpoint_to_process:
            update_endpoint(endpoint)

    return True
