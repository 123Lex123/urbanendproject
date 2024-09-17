
from django.urls import path
from .views import index, poll, register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('poll/<int:question_id>/', poll, name='poll'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', register, name='register'),
]
