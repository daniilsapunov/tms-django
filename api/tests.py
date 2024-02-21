from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from polls.models import Question, Choice
from shop.models import Category, Product
from articles.views import Article


class BaseAPITest(TestCase):
    # endpoint = None
    # model = None

    def assert_no_results(self, response):
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['results'], [])

    def assert_results_exist(self, response):
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json()['results'], [])

    def assert_nonexistent_detail(self, response):
        self.assertEquals(response.status_code, 404)

    def assert_detail_data(self, response, expected_data, arg=None):
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()[arg], expected_data)


class QuestionTests(BaseAPITest):
    # endpoint = '/api/questions/'
    # model = Question

    def test_no_questions(self):
        response = self.client.get('/api/questions/')
        self.assert_no_results(response)

    def test_question(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        response = self.client.get('/api/questions/')
        self.assert_results_exist(response)

    def test_nonexistent_question_detail(self):
        response = self.client.get('/api/questions/1/')
        self.assert_nonexistent_detail(response)

    def test_question_detail(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        response = self.client.get(f'/api/questions/{question.id}/')
        expected_data = question.question_text
        arg = 'question_text'
        self.assert_detail_data(response, expected_data, arg)


class ChoiceTests(BaseAPITest):
    def test_no_questions(self):
        response = self.client.get('/api/choices/')
        self.assert_no_results(response)

    def test_question(self):
        q = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        c = Choice.objects.create(question=q, choice_text='YES')

        response = self.client.get('/api/choices/')
        self.assert_results_exist(response)

    def test_nonexistent_choice_detail(self):
        response = self.client.get('/api/choices/1/')
        self.assert_nonexistent_detail(response)

    def test_choice_detail(self):
        q = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        c = Choice.objects.create(question=q, choice_text='YES')

        response = self.client.get(f'/api/choices/{c.id}/')
        expected_data = c.choice_text
        arg = 'choice_text'
        self.assert_detail_data(response, expected_data, arg)


class ArticleTests(BaseAPITest):
    def test_no_articles(self):
        response = self.client.get('/api/articles/')
        self.assert_no_results(response)

    def test_articles(self):
        a = Article.objects.create(title='t', pub_date=timezone.now() + timezone.timedelta(days=3),
                                   text='t')

        response = self.client.get('/api/articles/')
        self.assert_results_exist(response)

    def test_nonexistent_articles_detail(self):
        response = self.client.get('/api/articles/1/')
        self.assert_nonexistent_detail(response)

    def test_articles_detail(self):
        a = Article.objects.create(title='t', pub_date=timezone.now() + timezone.timedelta(days=3),
                                   text='t')
        response = self.client.get(f'/api/articles/{a.id}/')
        expected_data = a.text
        arg = 'text'
        self.assert_detail_data(response, expected_data, arg)


class ProductTests(BaseAPITest):
    def test_no_products(self):
        response = self.client.get('/api/products/')
        self.assert_no_results(response)

    def test_products(self):
        c = Category.objects.create(name='abc')
        p = Product.objects.create(name='t', description='t',
                                   price=100, category=c)

        response = self.client.get('/api/products/')
        self.assert_results_exist(response)

    def test_nonexistent_products_detail(self):
        response = self.client.get('/api/products/1/')
        self.assert_nonexistent_detail(response)

    def test_products_detail(self):
        c = Category.objects.create(name='abc')
        p = Product.objects.create(name='t', description='t',
                                   price=100, category=c)

        response = self.client.get(f'/api/products/{p.id}/')
        expected_data = p.name
        arg = 'name'
        self.assert_detail_data(response, expected_data, arg)


class CategoryTests(BaseAPITest):
    def test_no_category(self):
        response = self.client.get('/api/categories/')
        self.assert_no_results(response)

    def test_category(self):
        c = Category.objects.create(name='abc')

        response = self.client.get('/api/categories/')
        self.assert_results_exist(response)

    def test_nonexistent_products_detail(self):
        response = self.client.get('/api/categories/1/')
        self.assert_nonexistent_detail(response)

    def test_products_detail(self):
        c = Category.objects.create(name='abc')

        response = self.client.get(f'/api/categories/{c.id}/')
        expected_data = c.name
        arg = 'name'
        self.assert_detail_data(response, expected_data, arg)


class APITestCase(BaseAPITest):
    def test_search(self):
        question1 = Question.objects.create(question_text='first', pub_date=timezone.now())
        question2 = Question.objects.create(question_text='second', pub_date=timezone.now())

        response = self.client.get('/api/questions/', {'search': 'second'})
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(response)
        # print(response.json())
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.assertEqual(response.status_code, 200)

        # Проверка наличия ожидаемых результатов поиска

    def test_sorting(self):
        question1 = Question.objects.create(question_text='c', pub_date=timezone.now())
        question2 = Question.objects.create(question_text='b', pub_date=timezone.now())
        question3 = Question.objects.create(question_text='a', pub_date=timezone.now())

        response = self.client.get('/api/questions/', {'ordering': '-question_text'})
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(response)
        # print(response.json())
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.assertEqual(response.status_code, 200)
        # Проверка правильности сортировки в ответе

    def test_pagination(self):
        question1 = Question.objects.create(question_text='c', pub_date=timezone.now())
        question2 = Question.objects.create(question_text='b', pub_date=timezone.now())
        question3 = Question.objects.create(question_text='a', pub_date=timezone.now())

        response = self.client.get('/api/questions/', {'page': 1, 'page_size': 1})
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(response)
        # print(response.json())
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.assertEqual(response.status_code, 200)
        # Проверка корректной пагинации и количества элементов на странице

    def test_min_max(self):
        q1 = Question.objects.create(question_text='c', pub_date=timezone.now())
        q2 = Question.objects.create(question_text='b', pub_date=timezone.now())
        c1 = Choice.objects.create(question=q1, choice_text='YES')
        c2 = Choice.objects.create(question=q1, choice_text='NO')
        c3 = Choice.objects.create(question=q2, choice_text='KYS')

        response_max = self.client.get('/api/questions/', {'max_choice_count': 1})
        response_min = self.client.get('/api/questions/', {'min_choice_count': 2})

        self.assertEqual(response_max.status_code, 200)
        self.assertEqual(response_min.status_code, 200)
        # Проверка корректной пагинации и количества элементов на странице

    def test_question_text(self):
        q1 = Question.objects.create(question_text='c', pub_date=timezone.now())
        q2 = Question.objects.create(question_text='b', pub_date=timezone.now())
        q3 = Question.objects.create(question_text='C', pub_date=timezone.now())
        c1 = Choice.objects.create(question=q1, choice_text='YES')
        c2 = Choice.objects.create(question=q1, choice_text='NO')
        c3 = Choice.objects.create(question=q2, choice_text='KYS')

        response_1 = self.client.get('/api/questions/', {'question_text': "c"})
        response_2 = self.client.get('/api/questions/', {'question_text': "b"})
        response_3 = self.client.get('/api/questions/', {'question_text': "C"})
        #
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(response_1)
        # print(response_2)
        # print(response_3)
        # print(response_1.json())
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(response_2.json())
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(response_3.json())
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_3.status_code, 200)
        # Проверка корректной пагинации и количества элементов на странице


# class TestPostPutDelete(TestCase):
#
#     def test_create_question(self):
#         data = {
#             'question_text': 'New Question',
#             'pub_date': timezone.now(),
#             'status': 'New',
#             'choices': [  # Предоставление выборов в виде списка словарей
#                 {'choice_text': 'Choice 1'},
#                 {'choice_text': 'Choice 2'}
#             ]
#         }
#         response = self.client.post(reverse('question-list'), data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Question.objects.count(), 1)
#         self.assertEqual(Question.objects.get().question_text, 'New Question')

def test_put(self):
    pass


def test_detele(self):
    pass
