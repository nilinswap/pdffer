from proj import settings
from constants import API_KEY

class ApiAuthMiddleware(object):
    # One-time configuration and initialization.

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        api_key_secret = request.headers.get(API_KEY)
        if api_key_secret == settings.API_KEY_SECRET:
            request.is_authenticated = True
        else:
            request.is_authenticated = False

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

