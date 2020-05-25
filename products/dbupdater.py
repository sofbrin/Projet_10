import requests
from django.core.exceptions import ObjectDoesNotExist
from products.models import CategoryDb, ProductDb


def check_categories():
    db_cat = CategoryDb.objects.select_cat()

    response = requests.get('https://fr.openfoodfacts.org/categories.json')
    data = response.json()
    api_cat = data['tags']

    for category in api_cat:
        if category['name'] in db_cat:
            update_products(category)


def update_products(category):
    print(category['name'])
    db_prod = ProductDb.objects.select_prod(category)

    page = 1
    response = requests.get('https://world.openfoodfacts.org/cgi/search.pl', params={
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': category['id'],
        'json': 1,
        'page_size': 50,
        'action': 'process',
        'page': page
    })
    data = response.json()
    api_prod = data['products']

    for product in api_prod:
        if product['url'] in db_prod:
            save_product(product)

    page += 1


def save_product(api_product):
    db_product = ProductDb.objects.get_prod(api_product)

    db_product.nutriscore = api_product['nutrition_grades']
    db_product.image = api_product['image_front_url']
    db_product.fat = api_product['nutriments']['fat']
    db_product.saturated_fat = api_product['nutriments']['saturated-fat']
    db_product.sugar = api_product['nutriments']['sugars']
    db_product.salt = api_product['nutriments']['salt']
    db_product.save()
    print('\nLe produit ' + db_product.name + ' a été mis à jour.')
