from django.db import models
from django.contrib import admin

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    date_of_birth = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Article(models.Model):
    text = models.TextField(max_length=300)
    pub_date = models.DateTimeField(verbose_name="date published")
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)

    @admin.display(
        boolean=True,
        description='is popular'
        # ordering='like_count'
    )
    def is_popular(self):
        return self.likes > 100

    def __str__(self):
        return self.title