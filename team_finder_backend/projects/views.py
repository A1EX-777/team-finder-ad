# projects/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Project
from .forms import ProjectForm


class ProjectListView(ListView):
    """Вывести список всех проектов"""

    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    ordering = ['-created_at']


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Создать новый проект"""

    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.participants.add(self.request.user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.object.pk})


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'
    pk_url_kwarg = 'project_id'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.object.pk})


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/favorite_projects.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        return self.request.user.favorites.all()


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.interested_users.filter(pk=request.user.pk).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({'status': 'ok', 'favorited': favorited})


@login_required
@require_POST
def toggle_participate(request, project_id):
    """Присоединиться/отказаться от участия в проекте"""

    project = get_object_or_404(Project, pk=project_id)
    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        participated = False
    else:
        project.participants.add(request.user)
        participated = True

    return JsonResponse({
        'status': 'ok',
        'participated': participated,
        'participant': participated,
        'participants_count': project.participants.count()
    })


@login_required
@require_POST
def complete_project(request, project_id):
    """Завершить проект (только для владельца)"""

    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if project.status == 'closed':
        return JsonResponse(
            {'status': 'error', 'message': 'Проект уже завершён'},
            status=400
        )
    project.status = 'closed'
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': 'closed'})
