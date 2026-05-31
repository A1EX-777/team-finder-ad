from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView

from team_finder.constants import PROJECTS_PAGINATE_BY

from .forms import UserEditForm

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'users'
    paginate_by = PROJECTS_PAGINATE_BY
    ordering = ['-date_joined']

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_type = self.request.GET.get('filter')

        if filter_type and self.request.user.is_authenticated:
            user = self.request.user
            if filter_type == 'owners-of-favorite-projects':
                favorite_projects = user.favorites.all()
                queryset = User.objects.filter(
                    owned_projects__in=favorite_projects
                ).distinct()
            elif filter_type == 'owners-of-participating-projects':
                participating_projects = user.participating_projects.all()
                queryset = User.objects.filter(
                    owned_projects__in=participating_projects
                ).distinct()
            elif filter_type == 'interested-in-my-projects':
                my_projects = user.owned_projects.all()
                queryset = User.objects.filter(
                    favorites__in=my_projects
                ).distinct()
            elif filter_type == 'participants-of-my-projects':
                my_projects = user.owned_projects.all()
                queryset = User.objects.filter(
                    participating_projects__in=my_projects
                ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_filter'] = self.request.GET.get('filter', '')
        return context


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'users/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('users:profile', kwargs={'user_id': self.object.pk})


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse(
            'users:profile', kwargs={'user_id': self.request.user.pk}
        )


def logout_view(request):
    """Выход пользователя с редиректом на главную"""
    logout(request)
    return redirect('projects:list')
