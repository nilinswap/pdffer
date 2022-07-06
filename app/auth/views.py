from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from appmigrations.models import ApiToken, Client, Invite
import json
import uuid




@csrf_exempt
@require_http_methods(["PUT"])
def verify_invite(_, invite_id: str):
    print("invite_id", invite_id)
    try:
        _ = Invite.objects.get(id=invite_id)
    except Invite.DoesNotExist:
        return JsonResponse(data={}, status=404)
    return JsonResponse(data={}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def create_client(request):
    content = json.loads(request.body)
    if 'email' not in content or 'password' not in content:
        return JsonResponse(data={}, status=400)
    
    try:
        client = Client.objects.create(
            email=content['email'],
            password=content['password'],
        )
        client.save()
        # api_key = uuid.uuid4().hex 

        # api_token = ApiToken.objects.create(client = client, api_key = api_key)
        # print('api_token', api_token)
    except IntegrityError as ie:
        print('ie', ie)
        return JsonResponse(data={}, status=400)

    return JsonResponse(data={}, status=201)