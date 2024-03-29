from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Choice
from django.http import Http404
from .forms import QuestionForm
from django.views.decorators.cache import cache_page
# Create your views here.


def index(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    context = {'latest_question_list': questions,}
    return render(request, 'polls/index.html', context)


def detail(request, question_id: int):
    #question = get_object_or_404(Question, id=question_id)
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    context = {'question': question}
    return render(request, 'polls/detail.html', context)


def vote(request, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choices.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'error_message': "You didn't select a choice",
            'question': question,
        })
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('polls:results', question.id)


def results(request, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    context = {'question': question}
    return render(request, 'polls/results.html', context)


def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            pub_date = form.cleaned_data['publication_date']
            question = Question(question_text=question_text, pub_date=pub_date)
            question.save()
            for choice_text in form.cleaned_data['choices'].split('\n'):
                question.choices.create(choice_text=choice_text, votes=0)
            return redirect('polls:detail', question.id)
    else:
        form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': form})
