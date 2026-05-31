# users/forms.py
from django import forms
from django.contrib.auth import get_user_model

from team_finder.mixins import GitHubURLValidationMixin

User = get_user_model()


class TeamFinderRegistrationForm(forms.ModelForm):
    """Переопределение формы регистрации"""

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password')

    def clean_email(self):
        """Проверка на уникальность email"""

        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return email

    def save(self, commit=True):
        """Сохранение пользователя с заполнением пароля"""

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class TeamFinderAuthorizationForm(forms.Form):
    """Форма авторизации"""

    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        # Принимает request из LoginView
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError('Неверный имейл или пароль')

            if not user.check_password(password):
                raise forms.ValidationError('Неверный имейл или пароль')

            if not user.is_active:
                raise forms.ValidationError('Учётная запись не активна')

            self.user_cache = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)


class UserEditForm(GitHubURLValidationMixin, forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = User
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')

    def clean_phone(self):
        """Валидация и нормализация номера телефона"""
        phone = self.cleaned_data.get('phone')

        if phone:
            if phone.startswith('8') and len(phone) == 11:
                phone = '+7' + phone[1:]

            # Проверка формата +7XXXXXXXXXX
            if not (phone.startswith('+7') and len(phone) == 12
                    and phone[2:].isdigit()):
                raise forms.ValidationError(
                    'Номер телефона должен быть в формате 8XXXXXXXXXX '
                    'или +7XXXXXXXXXX'
                )

            # Проверка уникальности
            if User.objects.exclude(pk=self.instance.pk).filter(
                    phone=phone).exists():
                raise forms.ValidationError(
                    'Пользователь с таким номером телефона уже существует'
                )
        return phone
