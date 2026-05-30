# users/models.py
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont
import random
import io


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            surname=surname,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self, email, name, surname, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **extra_fields)


class User(AbstractUser):
    """
    Модифицированная модель пользователя
    is_active, is_staff - стандартные поля модели AbstractUser
    """

    email = models.EmailField(verbose_name='Почта', unique=True, blank=False)
    name = models.CharField(verbose_name='Имя', max_length=124, blank=False)
    surname = models.CharField(
        verbose_name='Фамилия', max_length=124, blank=False
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='avatars/',
        blank=True,
        null=True,
    )
    phone = models.CharField(
        verbose_name='Телефон', max_length=12, blank=False
    )
    github_url = models.URLField(
        verbose_name='GitHub URL', max_length=256, blank=True
    )
    about = models.TextField(verbose_name='О себе', max_length=256, blank=True)
    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True,
        verbose_name='Избранные проекты'
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def save(self, *args, **kwargs):
        # Генерирует аватар только при создании и если его нет
        if not self.pk and not self.avatar:
            self.avatar = self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        """Генерирует аватар с первой буквой имени"""
        # Размер аватара
        size = (200, 200)

        # Создает изображение
        image = Image.new('RGB', size, self._get_random_color())
        draw = ImageDraw.Draw(image)

        # Берет первую букву имени и делает её заглавной
        letter = self.name[0].upper()

        # Задает стандартный шрифт
        font = ImageFont.load_default()

        # Задаем размер текста
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Размещает текст по центру изображения
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2

        # Рисует букву на изображении
        draw.text((x, y), letter, fill='white', font=font)

        # Сохраняем в байтовый поток
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')

        # Возвращает файл для сохранения
        return ContentFile(buffer.getvalue(), name=f'avatar_{self.email}.png')

    def _get_random_color(self):
        """Возвращает случайный цвет"""
        r = random.randint(50, 200)
        g = random.randint(50, 200)
        b = random.randint(50, 200)
        return (r, g, b)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.name} {self.surname}"
