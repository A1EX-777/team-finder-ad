import http

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from team_finder.constants import (PROJECTS_ORDERING, PROJECTS_PAGINATE_BY,
                                   STATUS_CLOSED)

from .forms import ProjectForm
from .models import Project


class ProjectListView(ListView):
    """Вывести список всех проектов"""

    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = PROJECTS_PAGINATE_BY
    ordering = [PROJECTS_ORDERING]

    def get_queryset(self):
        return (Project.objects
                .select_related('owner')
                .prefetch_related('participants')
                .order_by(*self.ordering))


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
        return reverse(
            'projects:detail',
            kwargs={'project_id': self.object.pk}
        )


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
        return reverse(
            'projects:detail', kwargs={'project_id': self.object.pk}
        )


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/favorite_projects.html'
    context_object_name = 'projects'
    paginate_by = PROJECTS_PAGINATE_BY

    def get_queryset(self):
        return (self.request.user.favorites
                .select_related('owner')
                .prefetch_related('participants'))


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if (is_favorited := project.interested_users.filter(
            pk=request.user.pk).exists()):
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)

    return JsonResponse({'status': 'ok', 'favorited': not is_favorited})


@login_required
@require_POST
def toggle_participate(request, project_id):
    """Присоединиться/отказаться от участия в проекте"""

    project = get_object_or_404(Project, pk=project_id)

    if (is_participating := project.participants.filter(
            pk=request.user.pk).exists()):
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({
        'status': 'ok',
        'participated': not is_participating,
        'participant': not is_participating,
        'participants_count': project.participants.count()
    })


@login_required
@require_POST
def complete_project(request, project_id):
    """Завершить проект (только для владельца)"""

    project = get_object_or_404(Project, pk=project_id, owner=request.user)

    if project.status == STATUS_CLOSED:
        return JsonResponse(
            {'status': 'error', 'message': 'Проект уже завершён'},
            status=http.HTTPStatus.BAD_REQUEST
        )

    project.status = STATUS_CLOSED
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': STATUS_CLOSED})
