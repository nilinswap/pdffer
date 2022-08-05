from urllib.request import Request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from cauth.models import Client
import uuid, json
import base64
from xhtml2pdf import pisa
from django import forms

from cauth.auth_decorator import api_auth, page_auth


def valid_email(email: str):
    try:
        f = forms.EmailField()
        f.clean(email)
    except ValidationError as ve:
        print("ve", email, ve)
        return False
    return True



@page_auth(False)
def index(request):
    if hasattr(request, "client") and request.client:
        api_key = request.client.api_key
    else:
        api_key = None
    return render(
        request,
        "index.html",
        context={
            "api_key": api_key,
            "page_authenticated": request.is_page_authenticated,
        },
    )


@csrf_exempt
def signup(request):
    return render(
        request,
        "signup.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )


@csrf_exempt
def forgot_password(request):
    return render(
        request,
        "forgot_password.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )


@csrf_exempt
def login(request):
    next_url = request.GET["next"] if "next" in request.GET else '/'
    print("next_url", next_url)
    return render(
        request,
        "login.html",
        context={
            "page_authenticated": request.is_page_authenticated,
            "next_url": next_url,
        },
    )


@page_auth()
def a(request):
    return render(
        request,
        "a.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )


def please_verify_your_email(request):
    return render(
        request,
        "please_verify_your_email.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )


def reset_password_success(request):
    return render(
        request,
        "reset_password_success.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )


@require_http_methods(["GET"])
def healthcheck(_):
    return HttpResponse("lub dub")



def verify_email(request: Request):
    email = request.GET.get('email')
    print("email", email)
    try:
        if not valid_email(email):
            return JsonResponse(data={"success": True, "unique_email":False, "valid_email": False, "message": "invalid email"}, status=200)
        Client.objects.get(email=email)
        return JsonResponse(data={"success": True,"unique_email":False, "valid_email": True, "message": "email already exists"}, status=200)
    except Client.DoesNotExist:
        return JsonResponse(data={"success": True, "unique_email":True, "valid_email": True,  "message": "unique email found"}, status=200)
    except Exception as e:
        raise e
    


@csrf_exempt
@require_http_methods(["POST"])
@api_auth
def get_pdf_from_html(request):
    """
    :param request:
    :return:
    """
    content = json.loads(request.body)
    print("content", content)
    html_body = content["html"]
    filename = uuid.uuid4().hex + ".pdf"
    result_file_path = "/tmp/" + filename
    print(result_file_path)

    result_file = open(result_file_path, "w+b")

    pisa_status = pisa.CreatePDF(html_body, dest=result_file)

    pdf_s = result_file.read()

    print("pisa_status", pisa_status)
    print(type(pdf_s))
    # close output file
    result_file.close()  # close output file

    result_file = open(result_file_path, "rb")
    # return FileResponse(result_file, content_type="application/pdf")
    body = {
        "isBase64Encoded": True,
        "pdf": base64.b64encode(result_file.read()).decode("UTF-8"),
    }
    return JsonResponse(body)
