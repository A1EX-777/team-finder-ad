from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from team_finder.constants import (MAX_LEN_PROJECT_NAME, MAX_LEN_STATUS,
                                   STATUS_CHOICES, STATUS_OPEN)

User = get_user_model()


class Project(models.Model):
    """
    Модель проекта
    """

    name = models.CharField(
        verbose_name='Название проекта',
        max_length=MAX_LEN_PROJECT_NAME,
    )
    description = models.TextField(
        verbose_name='Описание проекта', blank=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True
    )
    github_url = models.URLField(
        verbose_name='GitHub URL', blank=True
    )
    status = models.CharField(
        verbose_name='Статус проекта',
        max_length=MAX_LEN_STATUS,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        User,
        related_name='participating_projects',
        blank=True
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'project_id': self.pk})
