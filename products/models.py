from django.db import models

from users.models import User


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class CategoryManager(models.Manager):
    def select_cat(self):
        return self.values_list('name', flat=True)


class CategoryDb(BaseModel):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    objects = CategoryManager()

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def select_prod(self, category):
        return self.filter(category_id__name=category).values_list('url', flat=True)

    def get_prod(self, product):
        return self.get(url=product['url'])


class ProductDb(BaseModel):
    DoesNotExist = None
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    image = models.URLField(max_length=255)
    nutriscore = models.CharField(max_length=255)
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    category = models.ForeignKey(CategoryDb, on_delete=models.CASCADE)

    objects = ProductManager()

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
