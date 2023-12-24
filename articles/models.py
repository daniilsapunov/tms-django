from django.db import models

# Create your models here.


class Article(models.Model):
    author_name = models.CharField(max_length=200)
    article_text = models.TextField(max_length=300)
    pub_date = models.DateTimeField(verbose_name="date published")
    article_name = models.CharField(max_length=100)

    def __str__(self):
        return self.article_name

