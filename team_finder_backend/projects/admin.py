from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'owner',
        'status', 'created_at',
        'description', 'github_url',
    )
    search_fields = ('name', 'description', 'owner__email')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Project, ProjectAdmin)
