
from django.http import JsonResponse


## A decorator
def api_auth(api_view):

    def decorator(request, *args, **kwargs):
        print("request", request.is_api_authenticated)
        if request.is_api_authenticated:
            return api_view(request, *args, **kwargs)        
        return JsonResponse(data={}, status = 403)
    
    return decorator
