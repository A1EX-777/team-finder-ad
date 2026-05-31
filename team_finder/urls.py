#  team_finder/urls.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include


urlpatterns = [
    path('', lambda request: redirect('projects/list/')),
    path('projects/', include('projects.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]
