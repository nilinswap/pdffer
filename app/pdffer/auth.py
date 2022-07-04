
from django.http import JsonResponse


def api_auth(api_view):

    def decorator(request):
        print("request", request.is_authenticated)
        if request.is_authenticated:
            return api_view(request)        
        return JsonResponse(data={}, status = 403)
    
    return decorator



