"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from apps.accounts.views import (
    CurrentSessionDeleteView,
    CurrentUserView,
    SessionCreateView,
    UserListView,
    UserRoleUpdateView,
    csrf_cookie,
)
from apps.comments.views import ProjectTaskCommentListCreateView
from apps.projects.views import (
    ProjectDetailView,
    ProjectEligibleMemberListView,
    ProjectListCreateView,
    ProjectMemberDetailView,
    ProjectMemberListView,
)
from apps.tasks.views import (
    ProjectTaskAssigneeDetailView,
    ProjectTaskAssigneesView,
    ProjectTaskDetailView,
    ProjectTaskListCreateView,
)
from config.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/csrf/", csrf_cookie, name="csrf-cookie"),
    path("api/health/", health_check, name="health-check"),
    path("api/projects/", ProjectListCreateView.as_view(), name="project-list"),
    path(
        "api/projects/<int:project_id>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "api/projects/<int:project_id>/members/",
        ProjectMemberListView.as_view(),
        name="project-member-list",
    ),
    path(
        "api/projects/<int:project_id>/eligible-members/",
        ProjectEligibleMemberListView.as_view(),
        name="project-eligible-member-list",
    ),
    path(
        "api/projects/<int:project_id>/members/<int:user_id>/",
        ProjectMemberDetailView.as_view(),
        name="project-member-detail",
    ),
    path(
        "api/projects/<int:project_id>/tasks/",
        ProjectTaskListCreateView.as_view(),
        name="project-task-list",
    ),
    path(
        "api/projects/<int:project_id>/tasks/<int:task_id>/",
        ProjectTaskDetailView.as_view(),
        name="project-task-detail",
    ),
    path(
        "api/projects/<int:project_id>/tasks/<int:task_id>/assignees/",
        ProjectTaskAssigneesView.as_view(),
        name="project-task-assignees",
    ),
    path(
        "api/projects/<int:project_id>/tasks/<int:task_id>/assignees/<int:user_id>/",
        ProjectTaskAssigneeDetailView.as_view(),
        name="project-task-assignee-detail",
    ),
    path(
        "api/projects/<int:project_id>/tasks/<int:task_id>/comments/",
        ProjectTaskCommentListCreateView.as_view(),
        name="project-task-comments",
    ),
    path("api/sessions/", SessionCreateView.as_view(), name="create-session"),
    path(
        "api/sessions/current/",
        CurrentSessionDeleteView.as_view(),
        name="delete-current-session",
    ),
    path("api/users/me/", CurrentUserView.as_view(), name="current-user"),
    path("api/users/", UserListView.as_view(), name="user-list"),
    path(
        "api/users/<int:user_id>/",
        UserRoleUpdateView.as_view(),
        name="user-role-update",
    ),
]
