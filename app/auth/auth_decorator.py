from django.http import JsonResponse, HttpResponseRedirect
from functools import wraps


## A decorator
def api_auth(api_view):
    def decorator(request, *args, **kwargs):
        print("request", request.is_api_authenticated)
        if request.is_api_authenticated:
            return api_view(request, *args, **kwargs)
        return JsonResponse(data={}, status=403)

    return decorator


## A decorator
def page_auth(redirect_to_login=True):
    def page_auth_factory(page_view):
        @wraps(page_view)
        def decorator(request, *args, **kwargs):
            print("request page auth", request.is_page_authenticated)
            if not request.is_page_authenticated and redirect_to_login:
                response = HttpResponseRedirect('/login') #TODO: should go with redirect url to the login page instead so that user is brought back to the resource that was denied. 
                response.delete_cookie('session_id')
                return response
            return page_view(request, *args, **kwargs)  
        return decorator
    return page_auth_factory
