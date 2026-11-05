from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task


class TaskCommentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.manager = User.objects.create_user(
            "manager@example.test",
            "test-password",
            role=User.Role.PROJECT_MANAGER,
        )
        self.member = User.objects.create_user(
            "member@example.test",
            "test-password",
            role=User.Role.DEVELOPER,
        )
        self.outsider = User.objects.create_user(
            "outsider@example.test",
            "test-password",
            role=User.Role.DEVELOPER,
        )
        self.admin = User.objects.create_user(
            "admin@example.test",
            "test-password",
            role=User.Role.ADMIN,
        )
        self.project = Project.objects.create(
            manager=self.manager,
            title="Comment project",
        )
        ProjectMember.objects.create(project=self.project, user=self.member)
        self.task = Task.objects.create(
            project=self.project,
            title="Comment task",
        )
        self.comments_url = (
            f"/api/projects/{self.project.pk}/tasks/{self.task.pk}/comments/"
        )

    def test_comment_author_and_timestamp_are_set_by_the_backend_and_persist(self):
        self.client.force_authenticate(self.member)
        response = self.client.post(
            self.comments_url,
            {"content": "First comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        created = response.json()
        self.assertEqual(created["author"]["userId"], self.member.pk)
        self.assertEqual(created["author"]["email"], self.member.email)
        self.assertTrue(created["createdAt"])
        self.assertEqual(created["taskId"], self.task.pk)

        reopened = self.client.get(self.comments_url)
        self.assertEqual(reopened.status_code, 200)
        self.assertEqual(reopened.json(), [created])

    def test_comments_are_listed_oldest_first(self):
        self.client.force_authenticate(self.member)
        first = self.client.post(
            self.comments_url,
            {"content": "First comment"},
            format="json",
        )
        second = self.client.post(
            self.comments_url,
            {"content": "Second comment"},
            format="json",
        )
        listed = self.client.get(self.comments_url)

        self.assertEqual(listed.status_code, 200)
        self.assertEqual(
            [comment["commentId"] for comment in listed.json()],
            [first.json()["commentId"], second.json()["commentId"]],
        )

    def test_blank_whitespace_and_oversized_comments_are_rejected(self):
        self.client.force_authenticate(self.member)
        for content in ("", "    \n\t", "x" * 2001):
            response = self.client.post(
                self.comments_url,
                {"content": content},
                format="json",
            )
            self.assertEqual(response.status_code, 400)
        self.assertEqual(self.task.comments.count(), 0)

    def test_client_cannot_supply_comment_author_or_timestamp(self):
        self.client.force_authenticate(self.member)

        response = self.client.post(
            self.comments_url,
            {
                "content": "Spoofed comment",
                "author": {"userId": self.manager.pk},
                "createdAt": "2000-01-01T00:00:00Z",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.task.comments.count(), 0)

    def test_user_without_project_access_cannot_read_or_add_comments(self):
        self.client.force_authenticate(self.outsider)

        self.assertEqual(self.client.get(self.comments_url).status_code, 404)
        self.assertEqual(
            self.client.post(
                self.comments_url,
                {"content": "Unauthorized"},
                format="json",
            ).status_code,
            404,
        )
        self.assertEqual(self.task.comments.count(), 0)

    def test_admin_can_read_comments_but_cannot_add_them(self):
        self.client.force_authenticate(self.admin)

        self.assertEqual(self.client.get(self.comments_url).status_code, 200)
        response = self.client.post(
            self.comments_url,
            {"content": "Admin comment"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.task.comments.count(), 0)
