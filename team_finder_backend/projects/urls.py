# projects/urls.py
from django.urls import path
from django.shortcuts import redirect
from . import views


app_name = 'projects'

urlpatterns = [
    path('', lambda request: redirect('list/')),
    path('list/', views.ProjectListView.as_view(), name='list'),
    path('create-project/', views.ProjectCreateView.as_view(), name='create'),
    path('<int:project_id>/', views.ProjectDetailView.as_view(), name='detail'),
    path(
        '<int:project_id>/edit/',
        views.ProjectUpdateView.as_view(),
        name='edit'
    ),
    path(
        '<int:project_id>/toggle-favorite/',
        views.toggle_favorite,
        name='toggle_favorite'
    ),
    path(
        '<int:project_id>/toggle-participate/',
        views.toggle_participate,
        name='toggle_participate'
    ),
    path('<int:project_id>/complete/', views.complete_project, name='complete'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
]
