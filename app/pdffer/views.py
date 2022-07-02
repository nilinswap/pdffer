from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .model_ops import get_nearest_shops, get_all_items
from django.views.decorators.http import require_http_methods
import traceback

def index(request):
    return render(request, 'index.html', context={})
 
@require_http_methods(["GET"])
def healthcheck(request):
    return HttpResponse("lub dub")


@require_http_methods(["GET"])
def find_shops_on_product(request):
    product_name = request.GET.get('productname', '').lower()
    try:
        shop_tuples = get_nearest_shops(product_name = product_name)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse(status=500)
    
    shops = [{'shop_name': shop_tuple[1], 'shop_address': shop_tuple[2]} for shop_tuple in shop_tuples]
    return JsonResponse({"data": shops})


@require_http_methods(["GET"])
def find_items_in_shop(request):
    shop_id = request.GET.get('shopid', '').lower()
    try:
        item_tuple = get_all_items(shop_id)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse(status=500)
    
    return JsonResponse({"data": item_tuple})
