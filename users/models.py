import io
import os
import random

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from team_finder import settings
from team_finder.constants import (AVATAR_FONT_SIZE, AVATAR_SIZE,
                                   AVATAR_TEXT_COLOR, FONT_PATHS,
                                   MAX_LEN_ABOUT, MAX_LEN_GITHUB_URL,
                                   MAX_LEN_USER_NAME, MAX_LEN_USER_PHONE,
                                   MAX_LEN_USER_SURNAME)

from .managers import UserManager


class User(AbstractUser):
    """
    Модифицированная модель пользователя
    is_active, is_staff - стандартные поля модели AbstractUser
    """

    username = None
    email = models.EmailField(verbose_name='Почта', unique=True, blank=False)
    name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LEN_USER_NAME,
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LEN_USER_SURNAME,
        blank=False
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='avatars/',
        blank=True,
        null=True,
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=MAX_LEN_USER_PHONE,
        blank=False
    )
    github_url = models.URLField(
        verbose_name='GitHub URL',
        max_length=MAX_LEN_GITHUB_URL,
        blank=True
    )
    about = models.TextField(
        verbose_name='О себе',
        max_length=MAX_LEN_ABOUT,
        blank=True
    )
    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True,
        verbose_name='Избранные проекты'
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        # Генерирует аватар только при создании и если его нет
        if not self.pk and not self.avatar:
            self.avatar = self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        """Генерирует аватар с первой буквой имени"""

        # Размер аватара
        size = AVATAR_SIZE

        color = self._get_random_color()

        image = Image.new('RGB', size, color)
        draw = ImageDraw.Draw(image)

        # Берет первую букву имени и делает её заглавной
        letter = self.name[0].upper()

        font = None
        for path in FONT_PATHS:
            if path.startswith('/'):
                full_path = path
            else:
                full_path = os.path.join(settings.BASE_DIR, path)

            if os.path.exists(full_path):
                try:
                    font = ImageFont.truetype(full_path, AVATAR_FONT_SIZE)
                    break
                except OSError:
                    continue

        if font is None:
            try:
                font = ImageFont.load_default(AVATAR_FONT_SIZE)
            except TypeError:
                font = ImageFont.load_default()

        # Задаем размер текста
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Размещает текст по центру изображения
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2

        # Рисует букву на изображении
        draw.text((x, y), letter, fill=AVATAR_TEXT_COLOR, font=font)

        # Сохраняем в байтовый поток
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')

        # Возвращает файл для сохранения
        return ContentFile(buffer.getvalue(), name=f'avatar_{self.email}.png')

    def _get_random_color(self):
        """Возвращает случайный цвет"""
        return tuple(random.randint(50, 200) for _ in range(3))
