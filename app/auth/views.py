from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from emailS.service import send_verification_email
from appmigrations.models import Client, Invite
import json
import datetime
from django.utils import timezone
from django.conf import settings


def send_email(client: Client):
    client_ekey = client.ekey
    verification_link = f"{settings.SITE_URL}/auth/verify_email/{client_ekey}"
    send_verification_email(email=client.email, verification_link=verification_link)


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
    print("rb", request.body)
    content = json.loads(request.body.decode("utf-8"))
    print("new_rb", request.body.decode("utf-8"))
    if "email" not in content or "password" not in content:
        return JsonResponse(data={}, status=400)

    try:
        client = Client.objects.create(
            email=content["email"],
            password=content["password"],
        )
        client.save()
        send_email(client)

        # api_key = uuid.uuid4().hex

        # api_token = ApiToken.objects.create(client = client, api_key = api_key)
        # print('api_token', api_token)
    except IntegrityError as ie:
        print("ie", ie)
        return JsonResponse(data={"success": False}, status=400)

    return JsonResponse(data={"success": True}, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_client(request):
    content = json.loads(request.body)
    email = content["email"]
    print("email", email)
    try:
        client = Client.objects.get(
            email=email,
        )
        client.delete()
        return JsonResponse(data={}, status=204)
    except IntegrityError as ie:
        print("ie", ie)
        return JsonResponse(data={}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def verify_email(_, client_ekey: str):
    try:
        client = Client.objects.get(ekey=client_ekey)
        if client.is_email_verified:
            pass
        elif client.created_on < (timezone.now() - datetime.timedelta(minutes=30)):
            ## TODO: keep a table of emails and their verification links and check if the link is still valid. Instead of doing it here, do it like this.
            return JsonResponse(
                data={"message": "Email verification link is expired"}, status=404
            )
        else:
            client.is_email_verified = True
            client.save()
        return HttpResponseRedirect("/")
    except Client.DoesNotExist:
        return JsonResponse(data={}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def verify_login(request):
    try:
        content = json.loads(request.body)
        if "email" not in content or "password" not in content:
            return JsonResponse(data={}, status=400)

        client = Client.objects.get(email=content["email"])
        if not client.is_email_verified:
            send_email(client)
            return HttpResponseRedirect("/auth/please_verify_your_email")
        elif client.password != content["password"]:
            return JsonResponse(data={}, status=400)
        return JsonResponse(data={'success': True}, status=200)
    except Client.DoesNotExist:
        return JsonResponse(data={}, status=404)
    except IntegrityError as ie:
        print("ie", ie)
        return JsonResponse(data={}, status=400)
