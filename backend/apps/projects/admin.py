from django.contrib import admin

from apps.projects.models import Project, ProjectMember

admin.site.register(Project)
admin.site.register(ProjectMember)
