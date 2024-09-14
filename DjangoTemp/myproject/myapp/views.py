from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Choice
from .forms import PollForm
from .models import Question


def index(request):
    latest_question_list = Question.objects.all()
    return render(request, 'myapp/index.html', {'latest_question_list': latest_question_list})


def poll(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question)

    if request.method == 'POST':
        selected_choice_id = request.POST.get('option')
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, pk=selected_choice_id)
            selected_choice.votes += 1
            selected_choice.save()
            return redirect('index')

    return render(request, 'myapp/poll.html', {
        'poll': {
            'question': question.question_text,
            'options': choices
        }
    })
