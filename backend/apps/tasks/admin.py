from django.contrib import admin

from apps.tasks.models import Task, TaskAssignee

admin.site.register(Task)
admin.site.register(TaskAssignee)
