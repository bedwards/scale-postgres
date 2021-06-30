from django.core.cache import cache


class LsnMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # look up LSN at the beginning of a user request
        request.lsn = cache.get(request.user.username)

        response = self.get_response(request)

        # save LSN at the end of a user request
        lsn = 0  # TODO: query postgres
        cache.set(request.user.username, lsn)

        return response
