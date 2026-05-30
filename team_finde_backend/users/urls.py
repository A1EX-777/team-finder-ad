# users/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView
from . import views
from .models import User
from .forms import CustomRegistrationForm, CustomAuthorizationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


app_name = 'users'

urlpatterns = [
    path('', lambda request: redirect('list/')),
    path('register/',
         CreateView.as_view(
             model=User,
             form_class=CustomRegistrationForm,
             template_name='users/register.html',
             success_url=reverse_lazy('projects:list')
         ),
         name='register'),
    path('login/',
         LoginView.as_view(
             form_class=CustomAuthorizationForm,
             template_name='users/login.html',
             redirect_authenticated_user=True,
         ),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/',
         PasswordChangeView.as_view(
             template_name='users/change_password.html',
             success_url=reverse_lazy('users:profile')
         ),
         name='change_password'),
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('<int:user_pk>/', views.UserDetailView.as_view(), name='profile'),
    path('edit-profile/', views.UserUpdateView.as_view(), name='edit_profile'),
]
