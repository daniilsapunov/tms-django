from django.contrib import admin
from .models import Category, Product, Order, OrderEntry, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderEntry)


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


class ProductInline(admin.StackedInline):
    model = Product
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
