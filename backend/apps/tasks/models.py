from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from apps.projects.models import Project


TASK_STATUS_VALUES = ("TODO", "IN_PROGRESS", "DONE")
TASK_PRIORITY_VALUES = ("LOW", "MEDIUM", "HIGH")


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "Por fazer"
        IN_PROGRESS = "IN_PROGRESS", "Em progresso"
        DONE = "DONE", "Concluída"

    class Priority(models.TextChoices):
        LOW = "LOW", "Baixa"
        MEDIUM = "MEDIUM", "Média"
        HIGH = "HIGH", "Alta"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(3)],
    )
    description = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(2000)],
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="TaskAssignee",
        related_name="assigned_tasks",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["project_id", "status", "priority", "title", "id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(status__in=TASK_STATUS_VALUES),
                name="task_status_is_valid",
            ),
            models.CheckConstraint(
                condition=models.Q(priority__in=TASK_PRIORITY_VALUES),
                name="task_priority_is_valid",
            ),
        ]

    def __str__(self):
        return self.title


class TaskAssignee(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="assignee_links",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_assignment_links",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["task_id", "user_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["task", "user"],
                name="unique_task_assignee",
            ),
        ]

    def __str__(self):
        return f"{self.user} — {self.task}"
