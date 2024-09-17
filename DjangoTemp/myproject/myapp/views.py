from django.shortcuts import render, get_object_or_404, redirect
from .models import Choice
from .models import Question
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


def index(request):
    latest_question_list = Question.objects.all()
    return render(request, 'myapp/index.html', {'latest_question_list': latest_question_list})


def poll(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question)

    if not request.user.is_authenticated:
        return render(request, 'myapp/not_authenticated.html', {
            'message': "Авторизуйтесь, чтобы пройти опрос."
        })

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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})
