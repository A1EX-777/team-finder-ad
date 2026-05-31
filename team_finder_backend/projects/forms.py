# projects/forms.py
from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    """Форма создания и редактирования проекта"""

    STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('closed', 'Закрыт'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label='Статус',
        widget=forms.Select
    )

    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')

    def clean_github_url(self):
        """Валидация ссылки на GitHub"""

        url = self.cleaned_data.get('github_url')
        if url:
            if 'github.com' not in url:
                raise forms.ValidationError('Ссылка должна вести на GitHub')
            if not url.startswith((
                'https://github.com/', 'http://github.com/'
            )):
                raise forms.ValidationError(
                    'Введите корректный URL GitHub репозитория'
                )
        return url
