from typing import List
from django.db import connection
# from appmigrations.models import Shop

# GET_NEAREST_SHOPS_QUERY = 'SELECT products.id, shops.name, shops.address, shops.location FROM ((products INNER JOIN items ON products.id=items.product_id) INNER JOIN shops ON items.shop_id=shops.id) WHERE products.name=%s order by shops.location'
# GET_ALL_ITEMS_QUERY = 'SELECT products.name from items INNER JOIN products ON products.id=items.product_id where items.shop_id=%s'

# # given a product name - Get all shops such that they have an item of this product sorted by nearest.
# def get_nearest_shops(product_name: str):
#     with connection.cursor() as cursor:
#         cursor.execute(GET_NEAREST_SHOPS_QUERY, [product_name])
#         row = cursor.fetchall()
#         print("len", len(row))
#     return row


# def get_all_items(shop_id: int) -> List[str]:
#     with connection.cursor() as cursor:
#         cursor.execute(GET_ALL_ITEMS_QUERY, [shop_id])
#         row = cursor.fetchall()
#         print("len", len(row))
#     return [item[0] for item in row]


# def test():
#     shop = Shop.objects.get(name='Veera Groc')
#     products_in_shop = get_all_items(shop.id)
#     assert('pedigree' in products_in_shop)

#     shop = Shop.objects.get(name='Dalal ki Dukaan')
#     products_in_shop = get_all_items(shop.id)
#     assert('thermometer' in products_in_shop)
    
#     product_name = "pedigree"
#     shops = get_nearest_shops(product_name)
#     assert(len(shops) == 2)
#     assert(shops[0][1] == 'Bos Medic')
#     assert(shops[1][1] == 'Veera Groc')

#     product_name = "thermometer"
#     shops = get_nearest_shops(product_name)
#     assert(len(shops) == 2)
#     assert(shops[0][1] == 'Dalal ki Dukaan')   
#     assert(shops[1][1] == 'Bos Medic')  

# if __name__ == '__main__':
#     test()
