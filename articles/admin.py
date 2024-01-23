from django.contrib import admin
from .models import Article
# Register your models here.


admin.site.register(Article)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'likes', 'is_popular')
    search_fields = ('title', 'authors', 'text')
    readonly_fields = ('likes',)