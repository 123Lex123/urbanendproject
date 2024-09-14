from django.urls import path
from .views import index
from .views import poll

urlpatterns = [
    path('', index, name='index'),
    path('poll/<int:question_id>/', poll, name='poll')
]
