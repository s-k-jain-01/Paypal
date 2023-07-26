from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField()
    price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.product_name