from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('choices', views.ChoiceViewSet)
router.register('articles', views.ArticleViewSet)
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/vote', views.choice_vote),
    path('register/', views.register_user),
]




