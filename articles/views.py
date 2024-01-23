from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
# Create your views here.
from .models import Article


def index(request):
    articles = Article.objects.order_by('article_name')
    context = {'all_articles': articles}
    return render(request, 'articles/index.html', context)


def detail(request, article_id: int):
    #article = get_object_or_404(Article, id=article_id)
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise Http404('Article does not exist')
    context = {'article': article}
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
    like.like_count += 1
    like.save()
    return redirect('articles:detail', article.id)




