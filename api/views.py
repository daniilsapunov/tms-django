from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from api.serializers import QuestionSerializer, ChoiceSerializer
from polls.models import Question, Choice
from rest_framework import viewsets


# # Create your views here.
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('choices')
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


@api_view(['POST'])
def choice_vote(request: Request, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    choice_id = request.data['choice']
    selected_choice = question.choices.get(id=choice_id)

    selected_choice.votes += 1
    selected_choice.save()

    return redirect('question-detail', question_id)



