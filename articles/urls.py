from django.urls import path

from . import views


app_name = 'articles'
urlpatterns = [
    path('index', views.index, name='all_articles'),
    path('<int:article_id>', views.detail, name='detail'),
    path('<int:article_id>/like', views.like, name='like'),

]

