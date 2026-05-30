from django.db import models


class Project(models.Model):
    """
    Модель проекта
    """

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(verbose_name='Название проекта', max_length=200)
    description = models.TextField(
        verbose_name='Описание проекта', blank=True
    )
    owner = models.ForeignKey(
        'users.User',
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
        max_length=6,
        blank=False,
        default=STATUS_CHOICES,
    )
    participants = models.ManyToManyField(
        'users.User',
        related_name='participating_projects',
        blank=True
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name
