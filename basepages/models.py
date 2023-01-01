from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length = 200, blank= False)
    product_description = models.TextField(blank= False)
    def __str__(self):
        return self.product_name
        