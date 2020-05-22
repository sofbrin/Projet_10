from django.db import models

from users.models import User


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class SelectManager(models.Manager):
    def select_cat_names(self):
        return self.values_list('name', flat=True)

    def select_cat(self, category):
        return self.filter(name=category['name'])

    def get_cat(self, category):
        return self.get(name=category[1])

    def get_prod(self, product):
        return self.get(name=product['product_name'])


class CategoryDb(BaseModel):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    objects = SelectManager()

    def __str__(self):
        return self.name


class ProductDb(BaseModel):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    image = models.URLField(max_length=255)
    nutriscore = models.CharField(max_length=255)
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    category = models.ForeignKey(CategoryDb, on_delete=models.CASCADE)

    objects = SelectManager()

    def __str__(self):
        return self.name


class UserPersonalDb(BaseModel):
    original_product = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name='original_product')
    replaced_product = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name='replaced_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['original_product', 'replaced_product', 'user'], name='no_double')
        ]
