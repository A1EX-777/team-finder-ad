from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, reverse_lazy

urlpatterns = [
    path('',
         lambda request: redirect(reverse_lazy('projects:list')),
         name='home'
         ),
    path('projects/', include('projects.urls', namespace='projects')),
    path('users/', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls, name='admin'),
]
