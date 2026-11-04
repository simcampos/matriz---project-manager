from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory

from apps.accounts.models import User
from apps.accounts.permissions import (
    CanAccessProject,
    CanManageProject,
    CanUpdateTaskStatus,
)
from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task, TaskAssignee


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = User.objects.create_user(
            "developer@example.test",
            "demo-password",
            role=User.Role.DEVELOPER,
        )

    def get_csrf_token(self):
        response = self.client.get("/api/csrf/")
        self.assertEqual(response.status_code, 204)
        return self.client.cookies["csrftoken"].value

    def log_in(self):
        csrf_token = self.get_csrf_token()
        return self.client.post(
            "/api/sessions/",
            {"email": self.user.email, "password": "demo-password"},
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

    def test_login_profile_and_logout_require_and_invalidate_session(self):
        self.assertEqual(self.client.get("/api/users/me/").status_code, 401)

        response = self.log_in()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["email"], self.user.email)
        self.assertTrue(self.client.cookies["sessionid"]["httponly"])
        self.assertNotIn("password", response.json()["user"])

        profile = self.client.get("/api/users/me/")
        self.assertEqual(profile.status_code, 200)
        self.assertEqual(profile.json()["userId"], self.user.pk)

        csrf_token = self.get_csrf_token()
        logout_response = self.client.delete(
            "/api/sessions/current/",
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(logout_response.status_code, 204)
        self.assertEqual(self.client.get("/api/users/me/").status_code, 401)

    def test_invalid_credentials_return_the_same_generic_error(self):
        csrf_token = self.get_csrf_token()
        responses = [
            self.client.post(
                "/api/sessions/",
                {"email": "missing@example.test", "password": "demo-password"},
                format="json",
                HTTP_X_CSRFTOKEN=csrf_token,
            ),
            self.client.post(
                "/api/sessions/",
                {"email": self.user.email, "password": "incorrect-password"},
                format="json",
                HTTP_X_CSRFTOKEN=csrf_token,
            ),
        ]

        self.assertEqual([response.status_code for response in responses], [401, 401])
        self.assertEqual(
            [response.json()["message"] for response in responses],
            ["Email ou palavra-passe inválidos."] * 2,
        )
        self.assertNotIn("sessionid", self.client.cookies)

    def test_login_requires_csrf_token(self):
        response = self.client.post(
            "/api/sessions/",
            {"email": self.user.email, "password": "demo-password"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.client.get("/api/users/me/").status_code, 401)


class ProjectAuthorizationTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            "manager@example.test",
            "demo-password",
            role=User.Role.PROJECT_MANAGER,
        )
        self.member = User.objects.create_user(
            "member@example.test",
            "demo-password",
            role=User.Role.DEVELOPER,
        )
        self.other_user = User.objects.create_user(
            "other@example.test",
            "demo-password",
            role=User.Role.DEVELOPER,
        )
        self.admin = User.objects.create_user(
            "admin@example.test",
            "demo-password",
            role=User.Role.ADMIN,
        )
        self.project = Project.objects.create(
            manager=self.manager,
            title="Restricted project",
        )
        ProjectMember.objects.create(project=self.project, user=self.member)
        self.task = Task.objects.create(
            project=self.project,
            title="Assigned task",
        )
        TaskAssignee.objects.create(task=self.task, user=self.member)
        self.factory = APIRequestFactory()

    def permission_allows(self, permission_class, user, obj):
        request = self.factory.get("/")
        request.user = user
        return permission_class().has_object_permission(request, None, obj)

    def test_project_visibility_is_limited_to_manager_and_members(self):
        self.assertTrue(
            self.permission_allows(CanAccessProject, self.manager, self.project)
        )
        self.assertTrue(
            self.permission_allows(CanAccessProject, self.member, self.project)
        )
        self.assertFalse(
            self.permission_allows(
                CanAccessProject,
                self.other_user,
                self.project,
            )
        )
        self.assertFalse(
            self.permission_allows(CanAccessProject, self.admin, self.project)
        )

    def test_only_project_manager_can_manage_and_assigned_developer_can_update(self):
        self.assertTrue(
            self.permission_allows(CanManageProject, self.manager, self.task)
        )
        self.assertFalse(
            self.permission_allows(CanManageProject, self.member, self.task)
        )
        self.assertTrue(
            self.permission_allows(CanUpdateTaskStatus, self.manager, self.task)
        )
        self.assertTrue(
            self.permission_allows(CanUpdateTaskStatus, self.member, self.task)
        )
        self.assertFalse(
            self.permission_allows(
                CanUpdateTaskStatus,
                self.other_user,
                self.task,
            )
        )
