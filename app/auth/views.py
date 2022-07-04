from django.http import JsonResponse
from auth.auth_decorator import api_auth
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from appmigrations.models import ApiToken, Client
import json
import uuid


@csrf_exempt
@require_http_methods(["POST"])
def create_token(request):
    content = json.loads(request.body)
    if 'client_name' in content:
        client = Client.objects.create(name=content)
    else:
        return JsonResponse(data={}, status=400)
    
    api_key = uuid.uuid4().hex 
    while len(ApiToken.objects.filter(api_key = api_key)):
        api_key = uuid.uuid4().hex 

    api_token = ApiToken.objects.create(client = client, api_key = api_key)
    print('api_token', api_token)
    return JsonResponse(data={'api_token': api_key})


@csrf_exempt
@require_http_methods(["PUT"])
def verify_token(_, api_key: str):
    print("api_key", api_key)
    return JsonResponse(data={}, status=200)

    