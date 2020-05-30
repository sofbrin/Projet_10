import requests
from products.models import CategoryDb, ProductDb


class ProductUpdater:
    def __init__(self):
        self.url = 'https://world.openfoodfacts.org/cgi/search.pl'
        self.params = {
            'tagtype_0': 'countries',
            'tag_contains_0': 'contains',
            'tag_0': 'france',
            'tagtype_1': 'categories',
            'tag_contains_1': 'contains',
            'tag_1': '',
            'json': 1,
            'page_size': 1000,
            'action': 'process',
            'page': 1,
            'fields': 'product_name,url,image_front_url,nutrition_grades,nutriments'
        }

    def check_products(self, n_products):
        self.params['page_size'] = n_products
        db_cat = CategoryDb.objects.select_cat()

        for category in db_cat:
            self._update(category)

    def _update(self, category):
        print('\n' + '\033[34m' + category + '\033[0m')
        self.params['tag_1'] = category
        response = requests.get(self.url, params=self.params)
        data = response.json()
        api_prod = data['products']
        db_prod = ProductDb.objects.select_prod(category)

        for api_product in api_prod:
            if api_product['url'] in db_prod:
                url_prefix = "/".join(api_product.get("url", "").split("/")[:-1])
                try:
                    db_product = ProductDb.objects.get(url__startswith=url_prefix)
                    self._save(db_product, api_product)
                except ProductDb.DoesNotExist:
                    continue

    def _save(self, db_product, api_product):
        db_product.name = api_product.get('product_name', db_product.name)
        db_product.nutriscore = api_product.get('nutrition_grades', db_product.nutriscore)
        db_product.image = api_product.get('image_front_url', db_product.image)
        db_product.fat = api_product['nutriments'].get('fat', db_product.fat)
        db_product.saturated_fat = api_product['nutriments'].get('saturated-fat', db_product.saturated_fat)
        db_product.sugar = api_product['nutriments'].get('sugars', db_product.sugar)
        db_product.salt = api_product['nutriments'].get('salt', db_product.salt)
        db_product.save()
        print('\nLe produit ' + db_product.name + ' a été mis à jour.')
