from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

# Create your tests here.
from articles.models import Article, Author


# Create your tests here.


def create_article(text, days, title, likes):
    pub_date = timezone.now() + timezone.timedelta(days=days)
    return Article.objects.create(text=text, title=title, pub_date=pub_date,
                                  likes=likes)


class ArticleIndexViewTests(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse('articles:all_articles'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'No article are available')

    def test_new_article(self):
        article = create_article('test1', 3, 'test1', 100)
        response = self.client.get(reverse('articles:all_articles'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['all_articles'], [article, ])


class ArticleDetailViewTests(TestCase):
    def test_get_article_not_exists(self):
        response = self.client.get(reverse('articles:detail', args=[66]))
        self.assertEquals(response.status_code, 404)

    def test_get_article(self):
        a = Author.objects.create(first_name='drill', last_name='danil')
        new_article = Article.objects.create(title='test1', pub_date=timezone.now(),
                                             text='test1', likes=100)
        new_article.authors.add(a)
        print(new_article)
        article_id = new_article.id
        response = self.client.get(reverse('articles:detail', args=[article_id]))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'test1')


class ArticlePopularOrNo(TestCase):
    def test_1(self):
        a1 = create_article('test1', 1, 'test1', 1)
        self.assertFalse(a1.is_popular())

    def test_2(self):
        a2 = create_article('test2', 2, 'test2', 100)
        self.assertFalse(a2.is_popular())

    def test_3(self):
        a3 = create_article('test3', 3, 'test3', 300)
        self.assertTrue(a3.is_popular())
