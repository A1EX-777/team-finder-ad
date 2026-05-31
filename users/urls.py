from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy
from django.views.generic import CreateView

from . import views
from .forms import TeamFinderAuthorizationForm, TeamFinderRegistrationForm

User = get_user_model()

app_name = 'users'

urlpatterns = [
    path('register/',
         CreateView.as_view(
             model=User,
             form_class=TeamFinderRegistrationForm,
             template_name='users/register.html',
             success_url=reverse_lazy('projects:list')
         ),
         name='register'),
    path('login/',
         LoginView.as_view(
             form_class=TeamFinderAuthorizationForm,
             template_name='users/login.html',
             redirect_authenticated_user=True,
         ),
         name='login'),
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
    path('change-password/',
         views.UserPasswordChangeView.as_view(),
         name='change_password'),
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('<int:user_id>/', views.UserDetailView.as_view(), name='profile'),
    path('edit-profile/', views.UserUpdateView.as_view(), name='edit_profile'),
]
