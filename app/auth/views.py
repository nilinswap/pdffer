from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from emailS.errors import EmailVerificationError
from emailS import service as email_service
from appmigrations.models import Client, Invite, Session
import json
import datetime
from django.utils import timezone
from django.conf import settings
from auth.utils import set_cookie
import uuid
from typing import Dict, Any, Callable
from django.contrib.auth.hashers import make_password, check_password


def send_verification_email(client: Client):
    client_ekey = client.ekey
    verification_link = f"{settings.SITE_URL}/auth/verify_email/{client_ekey}"
    email_service.send_verification_email(email=client.email, verification_link=verification_link)


def sane_email_password_response(content: Dict[str, Any], handler: Callable[[Dict[str, Any]], JsonResponse], email_name = 'email', password_name = 'password'):
    if email_name not in content or password_name not in content:
        return JsonResponse(data={'success': False, 'message': 'request misses email or password'}, status=400)
    print("sane_email_password_request", content)
    return handler(content)


@csrf_exempt
@require_http_methods(["PUT"])
def verify_invite(_: HttpRequest, invite_id: str):
    try:
        _ = Invite.objects.get(id=invite_id)
    except Invite.DoesNotExist:
        return JsonResponse(data={"message": "not found", 'success': False}, status=404)
    return JsonResponse(data={'success': True}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def create_client(request: HttpRequest):
    def create_client_handler(content):
        try:
            salty_pass = make_password(content['password'])
            print("salty_pass", salty_pass, make_password(content['password']))
            client = Client.objects.create (
                email=content["email"],
                password=salty_pass,
                api_key=uuid.uuid4().hex,
            )
            client.save()
            send_verification_email(client)
        except IntegrityError as ie:
            print("ie", ie)
            return JsonResponse(data={"message": str(ie), "success": False}, status=400)
        except EmailVerificationError as eve:
            return JsonResponse(data={
                "success": False,
                "message": str(eve)
            }, status=500)

        return JsonResponse(data={"success": True}, status=201)

    content = json.loads(request.body.decode("utf-8"))
    return sane_email_password_response(content, create_client_handler)
    


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_client(request: HttpRequest):
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
def verify_email(_: HttpRequest, client_ekey: str):
    try:
        client = Client.objects.get(ekey=client_ekey)
        if client.is_email_verified:
            pass
        elif client.created_on < (timezone.now() - datetime.timedelta(minutes=30)):
            ## TODO: keep a table of emails and their verification links and check if the link is still valid. Instead of doing it here, do it based on delta of email sent and verification link clicked.
            return JsonResponse(
                data={
                    "message": "Email verification link is expired",
                    "success": False
                }, status=404
            )
        else:
            client.is_email_verified = True
            client.save()
        response = HttpResponseRedirect("/")
        session = Session.objects.create(client=client)
        set_cookie(response, 'session_id', session.ekey)
        return response
    except Client.DoesNotExist:
        return JsonResponse(data={
            "message": "not found",
            "success": False
        }, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def verify_login(request: HttpRequest):
    def verify_login_handler(content: Dict[str, Any]):
        try:
            client = Client.objects.get(email=content["email"])
            print("client", client.is_email_verified)
            if not client.is_email_verified:
                send_verification_email(client)
                return JsonResponse(data={'success': True, "location": "/please_verify_your_email", "message": "redirect to location"}, status=278)
            elif not check_password(content["password"], client.password):
                return JsonResponse(data={}, status=401)
            session = Session.objects.create(client=client)
            response = JsonResponse(data={'success': True}, status=200)
            set_cookie(response, 'session_id', session.ekey)
            print("response", response.cookies)
            return response
        except Client.DoesNotExist:
            return JsonResponse(data={}, status=404)
        except IntegrityError as ie:
            return JsonResponse(data={
                "success": False,
                "message": str(ie)
            }, status=400)
        except EmailVerificationError as eve:
            return JsonResponse(data={
                "success": False,
                "message": str(eve)
            }, status=500)
        
    content = json.loads(request.body.decode("utf-8"))
    return sane_email_password_response(content, verify_login_handler)


@csrf_exempt
@require_http_methods(["POST"])
def verify_session(request):
    try:
        content = json.loads(request.body)
        if "session_id" not in content:
            return JsonResponse(data={}, status=400)
        session = Session.objects.get(ekey=content["session_id"])
        if session.created_on < (timezone.now() - datetime.timedelta(days=7)):
            return JsonResponse(data={}, status=400)
        return JsonResponse(data={}, status=200)
    except Session.DoesNotExist:
        return JsonResponse(data={}, status=404)
    except IntegrityError as ie:
        print("ie", ie)
        return JsonResponse(data={}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def forgot_password(request: HttpRequest):
    email_name = 'email'
    password_name = 'new_password'
    def forgot_password_handler(content: Dict[str, Any]):
        try:
            client = Client.objects.get(email=content[email_name])
            client.password = make_password(content[password_name])
            client.save()
            response = JsonResponse(data={'success': True}, status=200)
            return response
        except Client.DoesNotExist:
            return JsonResponse(data={}, status=404)
        
    content = json.loads(request.body.decode("utf-8"))
    print('content', content)
    return sane_email_password_response(content, forgot_password_handler, email_name, password_name)