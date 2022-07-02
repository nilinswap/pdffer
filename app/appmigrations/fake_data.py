from django.db import transaction
from .models import Shop, ShopOwner, User, Item, Product, ShopType

SEED = 4321

import random
random.seed(SEED)


from faker import Faker
fake = Faker()
Faker.seed(SEED)

USER_NAMES = [
    "Sam Joseph",
    "Seth Veera",
    "Abhay Prakash",
    "Bos Paren",
    "Beta Dalal",
]
OWNERS_NAMES = [
    "Seth Veera",
    "Bos Paren",
    "Beta Dalal",
]
SHOP_NAMES = [
    ("Seth Veera", "Veera Groc"),
    ("Bos Paren", "Bos Medic"),
    ("Beta Dalal", "Dalal ki Dukaan")
] 
PRODUCT_NAMES = [
'danish','cheesecake','sugar',
'Lollipop','wafer','Gummies',
'sesame','Jelly','beans',
'pie','bar','Ice','oat' ]

ITEM_DICT = {
    "pedigree" : ["Veera Groc", "Bos Medic"],
    "thermometer" : ["Dalal ki Dukaan", "Bos Medic"]
}
NUM_ITEMS = 20



@transaction.atomic
def populate_user():
    for name in USER_NAMES:
        user = User(
            name = name,
            email = fake.email(),
            password = fake.password(),
            aadhar_id = fake.bothify('#'*12),
            phone_number = fake.bothify('#'*10)
        )
        user.save()
        print(user)

@transaction.atomic
def populate_shop_owner():
    for name in USER_NAMES:
        shopOwner = ShopOwner(
            pan_card_id = fake.bothify("?????####?").upper(), 
            personal_address = fake.address(), 
            user_details = User.objects.get(name=name),
        )
        shopOwner.save()
        print(shopOwner)


@transaction.atomic
def populate_shop():
    for owner_name, shop_name in SHOP_NAMES:
        shop = Shop(
            name = shop_name,
            address = fake.address(),
            location = random.randint(4, 100),
            gst_number = fake.bothify('#'*20),
            type = random.choice(ShopType.values),
            owner = ShopOwner.objects.get(user_details__name=owner_name),
            phone_number = fake.bothify('#'*10),
            email = fake.email()
        )
        shop.save()
        print(shop)

@transaction.atomic
def populate_product():
    for product_name in PRODUCT_NAMES:
        product = Product(
            name = product_name,
            barcode = fake.bothify('?'*20),
            brand = fake.bothify('?'*5),
            description = fake.sentence(),
        )
        product.save()
        print(product)


@transaction.atomic
def populate_item_for_verfication():
        
    Product(name="pedigree", barcode = fake.bothify('?'*20),
            brand = fake.bothify('?'*5),
            description = fake.sentence()).save()

    Product(name="thermometer", barcode = fake.bothify('?'*20),
            brand = fake.bothify('?'*5),
            description = fake.sentence()).save()
    for product_name in ITEM_DICT:
        product = Product.objects.get(name = product_name)
        for shop_name in ITEM_DICT[product_name]:
            shop = Shop.objects.get(name = shop_name)
            Item(shop=shop, product=product).save()


@transaction.atomic
def propulate_items():
    shops = Shop.objects.all()
    products = Product.objects.all()
    for _ in range(NUM_ITEMS):
        item = Item(
            shop = random.choice(shops),
            product = random.choice(products),
        )
        item.save()
        print(item)
    populate_item_for_verfication()


@transaction.atomic
def populate():
    populate_user()
    populate_shop_owner()
    populate_shop()
    populate_product()
    propulate_items()

