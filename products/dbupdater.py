import requests
from django.core.exceptions import ObjectDoesNotExist
from products.models import CategoryDb, ProductDb


def check_categories():
    db_cat = CategoryDb.objects.select_cat_names()

    response = requests.get('https://fr.openfoodfacts.org/categories.json')
    data = response.json()
    api_cat = data['tags']

    shared_cats = {cat: api_cat[cat] for cat in api_cat if cat['name'] in db_cat and api_cat[cat]['name'] == db_cat[cat]['name']}
    print(len(shared_cats))

    """for cat in api_cat:
        if cat['name'] in db_cat and api_cat[cat]['name'] == db_cat['name']:
            check_products(cat['name'], db_cat(cat.name))

        else:
            print('1message d\'erreur')"""


def check_products(categoryApi, categoryDb):
    db_prod = ProductDb.objects.get_cat(categoryDb)
    print(db_prod)
    page = 1
    r_products = requests.get('https://world.openfoodfacts.org/cgi/search.pl', params={
        'tagtype': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': categoryApi['id'],
        'json': 1,
        'page_size': 50,
        'action': 'process',
        'page': page
    })
    response = r_products.json()
    api_prod = response['products']
    for prod in api_prod:
        if prod['name'] in db_prod and api_prod[prod]['product_name'] == db_prod[prod]['product_name']:
            compare_product(api_prod[prod], db_prod[prod])
        else:
            print('message d\'erreur')
    page += 1


def compare_product(api_product, db_product):
    #db_category = CategoryDb.objects.get_cat(category)
    ProductDb.objects.get_prod(db_product)

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
