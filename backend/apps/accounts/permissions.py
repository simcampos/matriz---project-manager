from rest_framework.permissions import BasePermission

from apps.accounts.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )


class IsProjectManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.PROJECT_MANAGER
        )


def get_related_project(obj):
    if hasattr(obj, "project"):
        return obj.project
    if hasattr(obj, "task"):
        return obj.task.project
    return obj


def can_access_project(user, project):
    if not user.is_authenticated or project is None:
        return False
    if user.role == User.Role.ADMIN:
        return True
    if (
        user.role == User.Role.PROJECT_MANAGER
        and project.manager_id == user.pk
    ):
        return True
    return project.member_links.filter(user_id=user.pk).exists()


def can_manage_project(user, project):
    return (
        user.is_authenticated
        and user.role == User.Role.PROJECT_MANAGER
        and project is not None
        and project.manager_id == user.pk
    )


class CanAccessProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return can_access_project(request.user, get_related_project(obj))


class CanManageProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return can_manage_project(request.user, get_related_project(obj))


class CanUpdateTaskStatus(BasePermission):
    def has_object_permission(self, request, view, task):
        if not can_access_project(request.user, task.project):
            return False
        if can_manage_project(request.user, task.project):
            return True
        return (
            request.user.role == User.Role.DEVELOPER
            and task.assignees.filter(pk=request.user.pk).exists()
        )
