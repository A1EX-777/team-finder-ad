# users/forms.py
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm
)
from .models import User


class CustomRegistrationForm(forms.ModelForm):
    """Переопределение формы регистрации"""

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password')


class CustomAvtorizationForm(forms.ModelForm):
    """Форма авторизации"""
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

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
        return self.cleaned_data


class UserEditForm(forms.ModelForm):
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
