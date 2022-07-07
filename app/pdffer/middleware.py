from proj import settings
from pdffer.constants import API_KEY
from auth.service import verify

class ApiAuthMiddleware(object):
    # One-time configuration and initialization.

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        api_key = request.headers.get(API_KEY)
        try:
            client_id = verify(api_key=api_key)
            if client_id:
                request.is_authenticated = True
            else:
                request.is_authenticated = False
        except Exception as e:
            raise e
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

