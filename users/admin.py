from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class TeamFinderUserAdmin(UserAdmin):
    """Класс для настройки отображения модели User в админке"""

    list_display = (
        'email', 'name', 'surname', 'phone', 'is_staff', 'is_active'
    )

    search_fields = ('email', 'name', 'surname', 'phone')

    list_filter = ('is_staff', 'is_active')

    ordering = ('email',)

    # Добавляем поля в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Персональная информация', {
            'fields': (
                'name', 'surname', 'phone', 'avatar', 'github_url', 'about'
            )
        }),
    )

    # Добавляем поля в форму создания
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Персональная информация', {
            'fields': (
                'email', 'name', 'surname', 'phone', 'github_url', 'about'
            )
        }),
    )
