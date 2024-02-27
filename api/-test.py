from django.test import TestCase
from django.utils import timezone
from polls.models import Question, Choice
from shop.models import Category, Product
from articles.views import Article


# class BaseAPITest(TestCase):
#     endpoint = None
#     model = None
#
#     def test_no_items(self):
#         response = self.client.get(self.endpoint)
#         self.assertEquals(response.status_code, 200)
#         self.assertEquals(response.json()['results'], [])
#
#     def test_item(self):
#         item = self.model.objects.create(title='t', pub_date=timezone.now())
#         response = self.client.get(self.endpoint)
#         self.assertEquals(response.status_code, 200)
#         self.assertNotEquals(response.json()['results'], [])
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['results'], [])

    def test_question(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json()['results'], [])

    def test_nonexistent_question_detail(self):
        response = self.client.get('/api/questions/1/')
        self.assertEquals(response.status_code, 404)

    def test_question_detail(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        response = self.client.get(f'/api/questions/{question.id}/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['question_text'], question.question_text)

    def test_no_choices(self):
        response = self.client.get('/api/choices/')
        self.assertEquals(response.json()['results'], [])

    def test_choice(self):
        q = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        c = Choice.objects.create(question=q, choice_text='YES')

        response = self.client.get('/api/choices/')
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json()['results'], [])

    def test_nonexistent_choice_detail(self):
        response = self.client.get('/api/questions/1/')
        self.assertEquals(response.status_code, 404)

    def test_choice_detail(self):
        q = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        c = Choice.objects.create(question=q, choice_text='YES')

        response = self.client.get(f'/api/choices/{c.id}/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['choice_text'], c.choice_text)


class TestAllApps(TestCase):
    def test_no_articles(self):
        response = self.client.get('/api/articles/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['results'], [])

    def test_articles(self):
        a = Article.objects.create(title='t', pub_date=timezone.now() + timezone.timedelta(days=3),
                                   text='t')

        response = self.client.get('/api/articles/')
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json()['results'], [])

    def test_nonexistent_article_detail(self):
        response = self.client.get('/api/articles/1/')
        self.assertEquals(response.status_code, 404)

    def test_article_detail(self):
        a = Article.objects.create(title='t', pub_date=timezone.now() + timezone.timedelta(days=3),
                                   text='t')
        response = self.client.get(f'/api/articles/{a.id}/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['text'], a.text)

    def test_product(self):
        response = self.client.get('/api/products/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['results'], [])

    def test_products(self):
        c = Category.objects.create(name='abc')
        p = Product.objects.create(name='t', description='t',
                                   price=100, category=c)

        response = self.client.get('/api/products/')
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json()['results'], [])

    def test_nonexistent_products_detail(self):
        response = self.client.get('/api/products/1/')
        self.assertEquals(response.status_code, 404)

    def test_article_detail(self):
        c = Category.objects.create(name='abc')
        p = Product.objects.create(name='t', description='t',
                                   price=100, category=c)
        response = self.client.get(f'/api/products/{p.id}/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['name'], p.name)

    def test_no_category(self):
        response = self.client.get('/api/categories/')
        self.assertEquals(response.status_code, 200)

    def test_category(self):
        c = Category.objects.create(name='abc')

        response = self.client.get('/api/categories/')
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json()['results'], [])

    def test_nonexistent_category_detail(self):
        response = self.client.get('/api/categories/1/')
        self.assertEquals(response.status_code, 404)

    def test_choice_detail(self):
        c = Category.objects.create(name='abc')

        response = self.client.get(f'/api/categories/{c.id}/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['name'], c.name)
