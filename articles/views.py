from random import randint

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
# Create your views here.
from .models import Article, Author
from django.utils import timezone
from datetime import datetime


def index(request):
    articles = Article.objects.all()
    context = {'all_articles': articles}
    return render(request, 'articles/index.html', context)


def detail(request, article_id: int):
    # article = get_object_or_404(Article, id=article_id)
    a = randint(1, 2)

    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise Http404('Article does not exist')
    try:
        author = Author.objects.get(article=article)
    except Author.MultipleObjectsReturned:
        author = Author.objects.filter(article=article)

    context = {'article': article, 'author': author}
    return render(request, 'articles/detail.html', context)


def like(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    try:
        like = Article.objects.get(id=article_id)
    except (KeyError, Article.DoesNotExist):
        return render(request, 'articles/detail.html', {
            'error_message': "i dont know",
            'article': article,
        })
    like.likes += 1
    like.save()
    return redirect('articles:detail', article.id)


def author_detail(request, author_id: id):
    author = get_object_or_404(Author, id=author_id)

    articles = Article.objects.filter(authors=author.id)
    context = {'author': author, 'articles': articles}
    return render(request, 'articles/author_detail.html', context)
