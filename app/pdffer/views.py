from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import uuid, json
import base64
from urllib3 import HTTPResponse
from xhtml2pdf import pisa

from cauth.auth_decorator import api_auth, page_auth


@page_auth()
def a(request: HttpRequest) -> HTTPResponse:
    return render(
        request,
        "pdffer/a.html",
        context={
            "page_authenticated": request.is_page_authenticated,
        },
    )


@page_auth(False)
def index(request: HttpRequest) -> HTTPResponse:
    if hasattr(request, "client") and request.client:
        api_key = request.client.api_key
    else:
        api_key = None
    return render(
        request,
        "pdffer/index.html",
        context={
            "api_key": api_key,
            "page_authenticated": request.is_page_authenticated,
        },
    )



@csrf_exempt
@require_http_methods(["POST"])
@api_auth
def get_pdf_from_html(request: HttpRequest) -> JsonResponse:
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


@require_http_methods(["GET"])
def healthcheck(_: HttpRequest) -> JsonResponse:
    return HttpResponse("lub dub")

