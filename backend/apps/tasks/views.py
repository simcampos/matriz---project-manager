from collections.abc import Mapping

from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import can_access_project, can_manage_project
from apps.projects.models import Project, ProjectMember
from apps.projects.serializers import ProjectMemberUserSerializer
from apps.tasks.models import Task, TaskAssignee
from apps.tasks.serializers import (
    TaskAssigneeCreateSerializer,
    TaskAssigneesUpdateSerializer,
    TaskCreateSerializer,
    TaskFilterSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
)


def get_accessible_project(user, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not can_access_project(user, project):
        raise Http404
    return project


def get_project_task(user, project_id, task_id):
    project = get_accessible_project(user, project_id)
    return get_object_or_404(
        project.tasks.prefetch_related("assignees"),
        pk=task_id,
    )


class ProjectTaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_accessible_project(request.user, project_id)
        filters = TaskFilterSerializer(data=request.query_params)
        filters.is_valid(raise_exception=True)

        tasks = project.tasks.prefetch_related("assignees")
        status_filter = filters.validated_data.get("status")
        priority_filter = filters.validated_data.get("priority")
        assignee_id = filters.validated_data.get("assignee_id")
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        if priority_filter:
            tasks = tasks.filter(priority=priority_filter)
        if assignee_id:
            tasks = tasks.filter(assignees__pk=assignee_id)

        return Response(TaskSerializer(tasks, many=True).data)

    def post(self, request, project_id):
        project = get_accessible_project(request.user, project_id)
        if not can_manage_project(request.user, project):
            return Response(
                {"detail": "Only the project manager can create tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.create(project=project, **serializer.validated_data)
        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED,
            headers={
                "Location": reverse(
                    "project-task-detail",
                    args=[project.pk, task.pk],
                )
            },
        )


class ProjectTaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, task_id):
        task = get_project_task(request.user, project_id, task_id)
        return Response(TaskSerializer(task).data)

    def patch(self, request, project_id, task_id):
        task = get_project_task(request.user, project_id, task_id)
        is_manager = can_manage_project(request.user, task.project)
        is_assigned_developer = (
            request.user.role == User.Role.DEVELOPER
            and task.assignees.filter(pk=request.user.pk).exists()
            and isinstance(request.data, Mapping)
            and set(request.data) == {"status"}
        )
        if not is_manager and not is_assigned_developer:
            return Response(
                {"detail": "You do not have permission to update this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TaskUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for field, value in serializer.validated_data.items():
            setattr(task, field, value)
        task.save()
        return Response(TaskSerializer(task).data)

    def delete(self, request, project_id, task_id):
        task = get_project_task(request.user, project_id, task_id)
        if not can_manage_project(request.user, task.project):
            return Response(
                {"detail": "Only the project manager can delete tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectTaskAssigneesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, task_id):
        task = get_project_task(request.user, project_id, task_id)
        assignees = task.assignees.all()
        return Response(ProjectMemberUserSerializer(assignees, many=True).data)

    def post(self, request, project_id, task_id):
        task = get_project_task(request.user, project_id, task_id)
        if not can_manage_project(request.user, task.project):
            return Response(
                {"detail": "Only the project manager can assign task users."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TaskAssigneeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if not user.is_active or not (
            user.pk == task.project.manager_id
            or ProjectMember.objects.filter(
                project=task.project,
                user=user,
            ).exists()
        ):
            return Response(
                {"userId": ["User is not eligible for this project."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                _, created = TaskAssignee.objects.get_or_create(
                    task=task,
                    user=user,
                )
        except IntegrityError:
            created = False
        if not created:
            return Response(
                {"detail": "This user is already assigned to the task."},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(
            ProjectMemberUserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, project_id, task_id):
        task = get_project_task(request.user, project_id, task_id)
        if not can_manage_project(request.user, task.project):
            return Response(
                {"detail": "Only the project manager can assign task users."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TaskAssigneesUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assignee_ids = serializer.validated_data["assigneeIds"]
        users = User.objects.filter(
            pk__in=assignee_ids,
            is_active=True,
        ).filter(
            Q(pk=task.project.manager_id)
            | Q(project_links__project=task.project)
        ).distinct()
        if users.count() != len(assignee_ids):
            return Response(
                {"assigneeIds": ["One or more users are not eligible."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        with transaction.atomic():
            task.assignees.set(users)
        return Response(ProjectMemberUserSerializer(users, many=True).data)


class ProjectTaskAssigneeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id, task_id, user_id):
        task = get_project_task(request.user, project_id, task_id)
        if not can_manage_project(request.user, task.project):
            return Response(
                {"detail": "Only the project manager can remove task users."},
                status=status.HTTP_403_FORBIDDEN,
            )
        assignment = get_object_or_404(
            TaskAssignee,
            task=task,
            user_id=user_id,
        )
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
