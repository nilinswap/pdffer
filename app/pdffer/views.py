from cgitb import reset
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from appmigrations.models import Session
import uuid, os, json
import base64
from xhtml2pdf import pisa

from auth.auth_decorator import api_auth


def index(request):
    ## use cookie in session_id and use it to fetch client_id and api_key. pass it here in context. 
    if 'session_id' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    else:
        session_ekey = request.COOKIES['session_id']
    
    try:
        session = Session.objects.get(ekey=session_ekey)
        client = session.client
        api_key = client.api_key
    except Session.DoesNotExist as sdne:
        print("sdne", sdne)
        response = HttpResponseRedirect('/')
        response.delete_cookie('session_id')
        return response
    except KeyError as ke:
        return HttpResponseRedirect('/login')
    return render(request, "index.html", context={"api_key": api_key})


@csrf_exempt
def signup(request):
    return render(request, "signup.html", context={})

@csrf_exempt
def forgot_password(request):
    return render(request, "forgot_password.html", context={})

@csrf_exempt
def login(request):
    return render(request, "login.html", context={})


def please_verify_your_email(request):
    return render(request, "please_verify_your_email.html", context={})
    

def reset_password_success(request):
    return render(request, "reset_password_success.html", context={})


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
