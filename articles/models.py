from django.db import models

# Create your models here.


class Article(models.Model):
    article_text = models.TextField(max_length=300)
    pub_date = models.DateTimeField(verbose_name="date published")
    article_name = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)

    def is_popular(self):
        return self.like_count > 100

    def __str__(self):
        return self.article_name


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    date_of_birth = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

