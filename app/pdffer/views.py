from cgitb import reset
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from appmigrations.models import Session
import uuid, os, json
import base64
from xhtml2pdf import pisa

from auth.auth_decorator import api_auth, page_auth


@page_auth(False)
def index(request):
    if hasattr(request, 'client') and request.client:
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
    return render(request, "signup.html", context={"page_authenticated": request.is_page_authenticated,})


@csrf_exempt
def forgot_password(request):
    return render(request, "forgot_password.html", context={"page_authenticated": request.is_page_authenticated,})


@csrf_exempt
def login(request):
    next_url = request.GET['next'] if 'next' in request.GET else None
    print("next_url", next_url)
    return render(request, "login.html", context={"page_authenticated": request.is_page_authenticated, 'next_url': next_url})


@page_auth()
def a(request):
    return render(request, "a.html", context={"page_authenticated": request.is_page_authenticated,})


def please_verify_your_email(request):
    return render(request, "please_verify_your_email.html", context={"page_authenticated": request.is_page_authenticated,})


def reset_password_success(request):
    return render(request, "reset_password_success.html", context={"page_authenticated": request.is_page_authenticated,})


@require_http_methods(["GET"])
def healthcheck(_):
    return HttpResponse("lub dub")


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
