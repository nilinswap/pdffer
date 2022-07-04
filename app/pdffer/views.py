from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .model_ops import get_nearest_shops, get_all_items
from django.views.decorators.http import require_http_methods
import traceback
import uuid, os, json
import base64
from xhtml2pdf import pisa

from .auth import api_auth


def index(request):
    return render(request, "index.html", context={})


@require_http_methods(["GET"])
def healthcheck(request):
    return HttpResponse("lub dub")


@require_http_methods(["GET"])
def find_shops_on_product(request):
    product_name = request.GET.get("productname", "").lower()
    try:
        shop_tuples = get_nearest_shops(product_name=product_name)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse(status=500)

    shops = [
        {"shop_name": shop_tuple[1], "shop_address": shop_tuple[2]}
        for shop_tuple in shop_tuples
    ]
    return JsonResponse({"data": shops})


@require_http_methods(["GET"])
def find_items_in_shop(request):
    shop_id = request.GET.get("shopid", "").lower()
    try:
        item_tuple = get_all_items(shop_id)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse(status=500)

    return JsonResponse({"data": item_tuple})


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
        'isBase64Encoded': True,
        'pdf': base64.b64encode(result_file.read()).decode('UTF-8')
    }
    return JsonResponse(body)

