from django import forms


class GitHubURLValidationMixin:
    """Миксин для валидации GitHub URL"""

    def clean_github_url(self):
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
