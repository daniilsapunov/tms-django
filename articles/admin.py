from django.contrib import admin
from .models import Article, Author


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('likes', 'is_popular')
    list_display = ('title', 'likes', 'is_popular', 'id')
    search_fields = ('title', 'authors', 'text', 'author__username')
    fieldsets = (
        (None, {
            'fields': ['title', 'authors', 'likes', 'is_popular', 'pub_date'],
        }),
        ('Content:', {
            'fields': ('text',),
        }),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth')
    search_fields = ('first_name', 'last_name')
