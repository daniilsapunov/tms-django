from django.core.management import BaseCommand
from polls.models import Question, Choice
from django.utils import timezone
import json


class Command(BaseCommand):
    help = 'Add question and choice'

    def add_arguments(self, parser):
        parser.add_argument('--data_file_path', type=str, required=False, default='data.json')

    def handle(self, *args, **options):
        Question.objects.all().delete()
        Choice.objects.all().delete()
        file = options['data_file_path']
        with open(file) as f:
            file_content = f.read()
            templates = json.loads(file_content)
        for i in templates:
            # print('Question = ', i)
            q = Question.objects.create(question_text=i, pub_date=timezone.now())
            for j in templates[i]:
                # print(j, templates[i].get(j))
                c = Choice.objects.create(question=q, choice_text=j, votes=int(templates[i].get(j)))
            # print()

    # populate_polls_database('data.json')
