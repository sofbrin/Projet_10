import requests
from django.core.exceptions import ObjectDoesNotExist
from products.models import CategoryDb, ProductDb


def check_categories():
    """response = requests.get('https://fr.openfoodfacts.org/categories.json')
    data = response.json()
    categories = data['tags']
    selected_cat = categories[50]
    for category in selected_cat:
        try:
            CategoryDb.objects.get(name=category['name'])

        except ObjectDoesNotExist:
            break"""

    db_cat = CategoryDb.objects.filter.values_list('name', flat=True)
    response = requests.get('https://fr.openfoodfacts.org/categories.json')
    data = response.json()
    api_cat = data['tags']
    for cat in api_cat:
        if cat in db_cat:
            check_products(cat)
        else:
            print('message d\'erreur')


def check_products(category):
    db_prod = ProductDb.objects.filter(category=category)
    page = 1
    r_products = requests.get('https://world.openfoodfacts.org/cgi/search.pl', params={
        'tagtype': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': category['id'],
        'page_size': 50,
        'action': 'process',
        'page': page
    })
    response = r_products.json()
    api_prod = response['products']
    for prod in api_prod:
        if prod in db_prod:
            compare_product(prod, category)
        else:
            print('message d\'erreur')
    page += 1


def compare_product(product, category):
    api_product = product
    db_category = CategoryDb.objects.get(name=category['name'])
    db_product = ProductDb.objects.get(name=product['product_name'], category=db_category)

    if api_product['nutrition_grades'] != db_product.nutriscore:
        db_product.nutriscore = api_product['nutrition_grades']
    if api_product['image_front_url'] != db_product.image:
        db_product.image = api_product['image_front_url']
    if api_product['nutriments']['fat'] != db_product.fat:
        db_product.fat = api_product['nutriments']['fat']
    if api_product['nutriments']['saturated-fat'] != db_product.saturated_fat:
        db_product.saturated_fat = api_product['nutriments']['saturated-fat']
    if api_product['nutriments']['sugars'] != db_product.sugar:
        db_product.sugar = api_product['nutriments']['sugars']
    if api_product['nutriments']['salt'] != db_product.salt:
        db_product.salt = api_product['nutriments']['salt']
    db_product.save()
    print('Le produit ' + db_product.name + ' de la catégorie ' + db_product.category + ' a été mis à jour.')









