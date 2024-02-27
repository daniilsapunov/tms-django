from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.main, name='main'),
    path('products', views.products_view, name='products_view'),
    path('products/<int:product_id>', views.product_detail, name='product_detail'),
    path('categories/<category_id>', views.category, name='all_of_category'),
    path('categories', views.categories, name='all_categories'),
    path('register', views.regform, name='register'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('shopping_cart', views.shopping_cart, name='shopping_cart'),
    path('clear_order', views.clear_order, name='clear_order'),
    path('clear_concrete_order', views.clear_concrete_order, name='clear_concrete_order'),
    path('update_count', views.update_count, name='update_count'),
    path('make_order', views.make_order, name='make_order'),
    path('success_order', views.success_order, name='success_order'),
    path('account', views.account, name='account'),
    path('order_history', views.order_history, name='order_history'),
    path('repeat_order', views.repeat_order, name='repeat_order'),

]
