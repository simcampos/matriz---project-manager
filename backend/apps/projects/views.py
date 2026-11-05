from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import can_manage_project
from apps.projects.models import Project, ProjectMember
from apps.projects.serializers import (
    ProjectCreateSerializer,
    ProjectMemberCreateSerializer,
    ProjectMemberUserSerializer,
    ProjectSerializer,
    ProjectUpdateSerializer,
)
from apps.tasks.models import TaskAssignee


def accessible_projects(user):
    if user.role == User.Role.ADMIN:
        return Project.objects.all()
    return Project.objects.filter(
        Q(manager=user) | Q(member_links__user=user)
    ).distinct()


def get_accessible_project(user, project_id):
    return get_object_or_404(accessible_projects(user), pk=project_id)


class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = accessible_projects(request.user)
        name = request.query_params.get("name")
        if name is not None:
            name = name.strip()
            if not name:
                return Response(
                    {"name": ["This field may not be blank."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            projects = projects.filter(title__icontains=name)

        return Response(ProjectSerializer(projects, many=True).data)

    def post(self, request):
        if request.user.role != User.Role.PROJECT_MANAGER:
            return Response(
                {"detail": "Only project managers can create projects."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.create(
            manager=request.user,
            **serializer.validated_data,
        )
        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_201_CREATED,
            headers={"Location": reverse("project-detail", args=[project.pk])},
        )


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, request, project_id):
        return get_accessible_project(request.user, project_id)

    def get(self, request, project_id):
        project = self.get_project(request, project_id)
        return Response(ProjectSerializer(project).data)

    def patch(self, request, project_id):
        project = self.get_project(request, project_id)
        if not can_manage_project(request.user, project):
            return Response(
                {"detail": "Only the project manager can edit this project."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProjectUpdateSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        project.title = serializer.validated_data.get("title", project.title)
        project.description = serializer.validated_data.get(
            "description",
            project.description,
        )
        project.save()
        return Response(ProjectSerializer(project).data)

    def delete(self, request, project_id):
        project = self.get_project(request, project_id)
        if not can_manage_project(request.user, project):
            return Response(
                {
                    "detail": "Only the project manager can delete this project."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectMemberListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_accessible_project(request.user, project_id)
        members = User.objects.filter(is_active=True).filter(
            Q(pk=project.manager_id) | Q(project_links__project=project)
        ).distinct()
        return Response(
            ProjectMemberUserSerializer(members, many=True).data
        )

    def post(self, request, project_id):
        project = get_accessible_project(request.user, project_id)
        if not can_manage_project(request.user, project):
            return Response(
                {"detail": "Only the project manager can add project members."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProjectMemberCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.pk == project.manager_id:
            return Response(
                {"detail": "The project manager is already an implicit member."},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            with transaction.atomic():
                _, created = ProjectMember.objects.get_or_create(
                    project=project,
                    user=user,
                )
        except IntegrityError:
            created = False

        if not created:
            return Response(
                {"detail": "This user is already a project member."},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(
            ProjectMemberUserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class ProjectEligibleMemberListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_accessible_project(request.user, project_id)
        if not can_manage_project(request.user, project):
            return Response(
                {"detail": "Only the project manager can add project members."},
                status=status.HTTP_403_FORBIDDEN,
            )

        existing_member_ids = ProjectMember.objects.filter(
            project=project,
        ).values("user_id")
        users = (
            User.objects.filter(is_active=True)
            .exclude(pk=project.manager_id)
            .exclude(pk__in=existing_member_ids)
        )
        return Response(ProjectMemberUserSerializer(users, many=True).data)


class ProjectMemberDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id, user_id):
        project = get_accessible_project(request.user, project_id)
        if not can_manage_project(request.user, project):
            return Response(
                {"detail": "Only the project manager can remove project members."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if user_id == project.manager_id:
            return Response(
                {"detail": "The project manager is an implicit member."},
                status=status.HTTP_409_CONFLICT,
            )

        membership = get_object_or_404(
            ProjectMember,
            project=project,
            user_id=user_id,
        )
        with transaction.atomic():
            TaskAssignee.objects.filter(
                task__project=project,
                user_id=user_id,
            ).delete()
            membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
