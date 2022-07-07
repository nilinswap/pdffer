from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import traceback
import uuid, os, json
import base64
from xhtml2pdf import pisa

from auth.auth_decorator import api_auth


def index(request):
    return render(request, "index.html", context={"api_key": "xyz"})


@csrf_exempt
def signup(request):
    return render(request, "signup.html", context={})

def please_verify_your_email(request):
    return render(request, "please_verify_your_email.html", context={})


@require_http_methods(["GET"])
def healthcheck(request):
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
