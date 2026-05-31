from django import forms

from team_finder.constants import STATUS_CHOICES
from team_finder.mixins import GitHubURLValidationMixin

from .models import Project


class ProjectForm(GitHubURLValidationMixin, forms.ModelForm):
    """Форма создания и редактирования проекта"""

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label='Статус',
        widget=forms.Select
    )

    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
