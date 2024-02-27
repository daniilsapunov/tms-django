from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.request import Request
from api.serializers import QuestionSerializer, ChoiceSerializer, CategorySerializer, ProductSerializer, \
    ArticleSerializer
from polls.models import Question, Choice
from articles.models import Article
from shop.models import Category, Product
from rest_framework import viewsets, filters, pagination
from .filters import ChoiceCountFilter, ArticlesCountWordFilter
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer


class DefaultPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class QuestionViewSet(viewsets.ModelViewSet):
    pagination_class = DefaultPagination
    queryset = Question.objects.prefetch_related('choices').order_by('-id')
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ChoiceCountFilter]
    ordering_fields = ['question_text', 'pub_date']
    search_fields = ['question_text']

    # filter_backends = [ChoiceCountFilter]


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all().order_by('-id')
    serializer_class = ChoiceSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['choice_text']
    search_fields = ['choice_text', 'question__question_text']


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ArticlesCountWordFilter]
    ordering_fields = ['text', 'authors']
    search_fields = ['title']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'price']
    search_fields = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name']
    search_fields = ['name']


@api_view(['POST'])
def choice_vote(request: Request, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    choice_id = request.data['choice']
    selected_choice = question.choices.get(id=choice_id)

    selected_choice.votes += 1
    selected_choice.save()

    return redirect('question-detail', question_id)


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
