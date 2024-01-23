from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    count = models.IntegerField(default=0)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order')

    def total(self):
        return  f'{self.count * self.product.price}'


    def __str__(self):
        #return f'{self.product} - {self.count} - {self.count * self.product.price}'
        return f'{self.product}'


class Order(models.Model):
    class Status(models.TextChoices):
        INITIAL = 'INITIAL'
        COMPLETED = 'COMPLETED'
        DELIVERED = 'DELIVERED'

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=200, default=Status.INITIAL, choices=Status.choices)

    def __str__(self):
        return f"{self.profile.user.username}-{self.status}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField(Order, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='+')

    def __str__(self):
        return f'{self.user.username}'
