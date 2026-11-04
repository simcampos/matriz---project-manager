import os
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from apps.accounts.models import User
from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task, TaskAssignee


class UserManagerTests(TestCase):
    def test_create_user_hashes_password_and_normalizes_email(self):
        user = User.objects.create_user(
            "Admin@Matriz.dev",
            "demo-password",
            role=User.Role.ADMIN,
        )

        self.assertEqual(user.email, "admin@matriz.dev")
        self.assertNotEqual(user.password, "demo-password")
        self.assertTrue(user.check_password("demo-password"))


class DemoSeedTests(TestCase):
    def test_seed_is_idempotent_and_does_not_replace_passwords(self):
        demo_env = {
            "DEMO_ADMIN_PASSWORD": "LocalAdminDemo-123",
            "DEMO_PM_PASSWORD": "LocalManagerDemo-123",
            "DEMO_DEVELOPER_PASSWORD": "LocalDeveloperDemo-123",
        }
        with patch.dict(os.environ, demo_env):
            call_command("seed_demo", stdout=StringIO())
            first_counts = (
                User.objects.count(),
                Project.objects.count(),
                ProjectMember.objects.count(),
                Task.objects.count(),
                TaskAssignee.objects.count(),
            )
            admin = User.objects.get(email="admin@matriz.dev")
            original_hash = admin.password

            call_command("seed_demo", stdout=StringIO())

        self.assertEqual(
            first_counts,
            (
                User.objects.count(),
                Project.objects.count(),
                ProjectMember.objects.count(),
                Task.objects.count(),
                TaskAssignee.objects.count(),
            ),
        )
        admin.refresh_from_db()
        self.assertEqual(admin.password, original_hash)
        self.assertTrue(admin.check_password(demo_env["DEMO_ADMIN_PASSWORD"]))
