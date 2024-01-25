from django.core.management import BaseCommand
from shop.models import Category, Product
from django.utils import timezone
from django.contrib.auth.models import User
import json


class Command(BaseCommand):
    help = 'Add product'

    def add_arguments(self, parser):
        parser.add_argument('--data_file_path', type=str, required=False, default='data_shop.json')

    def handle(self, *args, **options):
        file = options['data_file_path']
        with open(file) as f:
            file_content = f.read()
            templates = json.loads(file_content)
        for i in templates:
            print('Category = ', i)
            category = Category.objects.get_or_create(name=i)
            print(category[0])
            p = Product.objects.create(name=templates[i].get('name'),
                                       description=templates[i].get('description'),
                                       price=int(templates[i].get('price')),
                                       category=category[0])
            #category = Category.objects.filter(name=i)
            # for j in templates[i]:
            #     print(j, templates[i].get('name'))
            #     #print(category)

        # print()

# populate_polls_database('data.json')
