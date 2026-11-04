from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Project(models.Model):
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="managed_projects",
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "id"]

    def clean(self):
        if self.manager_id and self.manager.role != self.manager.Role.PROJECT_MANAGER:
            raise ValidationError({"manager": "Project manager must have the Project Manager role."})

    def __str__(self):
        return self.title


class ProjectMember(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="member_links",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_links",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["project_id", "user_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"],
                name="unique_project_member",
            ),
        ]

    def __str__(self):
        return f"{self.user} — {self.project}"
