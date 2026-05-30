# users/views.py
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import UserEditForm


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'users'
    paginate_by = 12
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
    template_name = 'users/user_details.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_pk'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'users/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={'user_pk': self.request.user.pk}
        )
