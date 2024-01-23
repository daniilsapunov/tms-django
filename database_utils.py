import json
from polls.models import Choice, Question
from django.utils import timezone


def populate_polls_database(name, clean_database=True):
    with open(name) as f:
        file_content = f.read()
        templates = json.loads(file_content)
    for i in templates:
        #print('Question = ', i)
        q = Question.objects.create(question_text=i, pub_date = timezone.now())
        for j in templates[i]:
            #print(j, templates[i].get(j))
            c = Choice.objects.create(question=q, choice_text=j, votes=int(templates[i].get(j)))
        #print()


#populate_polls_database('data.json')

