from pdffer.constants import API_KEY
from cauth.service import verify
from cauth.models import Session


class ApiAuthMiddleware(object):
    # One-time configuration and initialization.

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        session_id = request.COOKIES.get("session_id")
        if session_id:
            try:
                session = Session.objects.get(ekey=session_id)
                request.client = session.client
                request.is_page_authenticated = True

            except Session.DoesNotExist:
                request.is_page_authenticated = False
            except Exception as e:
                raise e
        else:
            request.is_page_authenticated = False

        api_key = request.headers.get(API_KEY)
        try:
            client_id = verify(api_key=api_key)
            if client_id:
                request.is_api_authenticated = True
                request.client_id = client_id
            else:
                request.is_api_authenticated = False
        except Exception as e:
            raise e
        response = self.get_response(request)

        return response
