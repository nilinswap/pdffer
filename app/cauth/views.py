from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from emailS.errors import EmailVerificationError
from emailS import service as email_service
from .models import Client, Invite, Session, VerificationEmailLinkEntry
import json
import datetime
from django.utils import timezone
from django.conf import settings
from cauth.utils import set_cookie
import uuid
from typing import Dict, Any, Callable
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from .utils import valid_email


def validate_email(request: HttpRequest) -> JsonResponse:
    email = request.GET.get("email")
    print("email", email)
    try:
        if not valid_email(email):
            return JsonResponse(
                data={
                    "success": True,
                    "unique_email": False,
                    "valid_email": False,
                    "message": "invalid email",
                },
                status=200,
            )
        Client.objects.get(email=email)
        return JsonResponse(
            data={
                "success": True,
                "unique_email": False,
                "valid_email": True,
                "message": "email already exists",
            },
            status=200,
        )
    except Client.DoesNotExist:
        return JsonResponse(
            data={
                "success": True,
                "unique_email": True,
                "valid_email": True,
                "message": "unique email found",
            },
            status=200,
        )
    except Exception as e:
        raise e


@csrf_exempt
def signup_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "cauth/signup.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )


@csrf_exempt
def forgot_password_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "cauth/forgot_password.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )




def please_verify_your_email_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "cauth/please_verify_your_email.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )


def reset_password_success_view(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "cauth/reset_password_success.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )
    


@csrf_exempt
def login_view(request: HttpRequest) -> HttpResponse:
    next_url = request.GET["next"] if "next" in request.GET else '/'
    print("next_url", next_url)
    return render(
        request,
        "cauth/login.html",
        context={
            "page_authenticated": request.is_page_authenticated,
            "next_url": next_url,
        },
    )



def send_verification_email(client: Client) -> None:
    client_ekey = client.ekey
    client = Client.objects.get(ekey=client_ekey)
    linkEntry = VerificationEmailLinkEntry(client = client)
    linkEntry.save()
    link = linkEntry.ekey
    verification_link = f"{settings.SITE_URL}/auth/api/verify_email/{link}"
    email_service.send_verification_email(email=client.email, verification_link=verification_link) 
    ## TODO: In the most ideal scenario, I should mark a linkEntry 'sent' after this and use that time to determine if the email has link that is valid. 



def sane_email_password_response(content: Dict[str, Any], handler: Callable[[Dict[str, Any]], JsonResponse], email_name = 'email', password_name = 'password') -> JsonResponse:
    if email_name not in content or password_name not in content:
        return JsonResponse(data={'success': False, 'message': 'request misses email or password'}, status=400)
    print("sane_email_password_request", content)
    return handler(content)


@csrf_exempt
@require_http_methods(["PUT"])
def verify_invite(_: HttpRequest, invite_id: str) -> JsonResponse:
    try:
        _ = Invite.objects.get(id=invite_id)
    except Invite.DoesNotExist:
        return JsonResponse(data={"message": "not found", 'success': False}, status=404)
    return JsonResponse(data={'success': True}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def create_client(request: HttpRequest) -> JsonResponse:
    def create_client_handler(content):
        try:
            salty_pass = make_password(content['password'])
            print("salty_pass", salty_pass, make_password(content['password']))
            client = Client.objects.create (
                email=content["email"],
                password=salty_pass,
                api_key=uuid.uuid4().hex,
            )
            print("client", client)
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
def delete_client(request: HttpRequest) -> JsonResponse:
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
def verify_email(_: HttpRequest, link_ekey: str) -> JsonResponse:
    try:
        linkEntry = VerificationEmailLinkEntry.objects.get(ekey=link_ekey)
        client = Client.objects.get(ekey=linkEntry.client.ekey)
        if client.is_email_verified:
            pass
        elif linkEntry.created_on < (timezone.now() - datetime.timedelta(minutes=30)):
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
def verify_login(request: HttpRequest) -> JsonResponse:
    def verify_login_handler(content: Dict[str, Any]):
        try:
            client = Client.objects.get(email=content["email"])
            print("client", client.is_email_verified)
            if not client.is_email_verified:
                send_verification_email(client)
                return JsonResponse(data={'success': True, "location": "/auth/please_verify_your_email", "message": "redirect to location"}, status=278)
            elif not check_password(content["password"], client.password):
                return JsonResponse(data={}, status=401)
            session = Session.objects.create(client=client)
            res_data = {'success': True}
            if 'next_url' in content:
                res_data['next_url'] = content['next_url']
            response = JsonResponse(data=res_data, status=200)
            set_cookie(response, 'session_id', session.ekey)
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
        except Exception as e:
            raise e
        
    content = json.loads(request.body.decode("utf-8"))
    return sane_email_password_response(content, verify_login_handler)


@csrf_exempt
@require_http_methods(["POST"])
def verify_session(request) -> JsonResponse:
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
        return JsonResponse(data={}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def forgot_password(request: HttpRequest) -> JsonResponse:
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
    return sane_email_password_response(content, forgot_password_handler, email_name, password_name)


@csrf_exempt
@require_http_methods(["GET"])
def logout(request: HttpRequest) -> HttpResponse:
    # read request cookie
    try:
        session_cookie = request.COOKIES.get('session_id')
        session = Session.objects.get(ekey=session_cookie)
        session.delete()
        response = HttpResponseRedirect('/auth/login') #TODO: should go with redirect url to the login page instead so that user is brought back to the resource that was denied. 
        response.delete_cookie('session_id')
        return response
    except Session.DoesNotExist:
        return HttpResponseRedirect('/')
