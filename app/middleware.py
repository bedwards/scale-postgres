import logging
from django.core.cache import cache
from . import database
from . import thread

logger = logging.getLogger(__name__)


class LsnMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # look up LSN at the beginning of a user request
            cached_primary_lsn = cache.get(request.user.username)
            thread.set_cached_primary_lsn(cached_primary_lsn)
            logger.error('LsnMiddleware before: cached primary LSN = %s',
                         cached_primary_lsn)

            response = self.get_response(request)

            if thread.did_write_happen():
                # save LSN at the end of a user request
                current_wal_lsn = database.get_current_wal_lsn()
                logger.error('LsnMiddleware after: caching primary LSN = %s',
                             current_wal_lsn)
                cache.set(request.user.username, current_wal_lsn)

        finally:
            thread.cleanup()

        return response
