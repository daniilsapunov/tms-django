from django.db import models

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_description = models.TextField


class Category(models.Model):
    category_name = models.CharField(max_length=50)
