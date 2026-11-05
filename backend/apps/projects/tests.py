from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.comments.models import Comment
from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task, TaskAssignee


class ProjectCascadeTests(TestCase):
    def test_deleting_project_cascades_through_demo_data_relations(self):
        manager = User.objects.create_user(
            "pm@example.test",
            "test-password",
            role=User.Role.PROJECT_MANAGER,
        )
        developer = User.objects.create_user(
            "developer@example.test",
            "test-password",
            role=User.Role.DEVELOPER,
        )
        project = Project.objects.create(manager=manager, title="Test project")
        ProjectMember.objects.create(project=project, user=developer)
        task = Task.objects.create(project=project, title="Test task")
        TaskAssignee.objects.create(task=task, user=developer)
        Comment.objects.create(task=task, author=developer, content="Test comment")
        project_id = project.pk
        task_id = task.pk

        project.delete()

        self.assertFalse(Project.objects.filter(pk=project_id).exists())
        self.assertFalse(Task.objects.filter(pk=task_id).exists())
        self.assertFalse(ProjectMember.objects.filter(project_id=project_id).exists())
        self.assertFalse(TaskAssignee.objects.filter(task_id=task_id).exists())
        self.assertFalse(Comment.objects.filter(task_id=task_id).exists())


class ProjectApiTests(TestCase):
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
            title="Alpha planning",
            description="First description",
        )
        ProjectMember.objects.create(project=self.project, user=self.member)

    def test_project_endpoints_require_authentication(self):
        self.assertEqual(self.client.get("/api/projects/").status_code, 401)
        self.assertEqual(self.client.post("/api/projects/").status_code, 401)
        self.assertEqual(
            self.client.get(f"/api/projects/{self.project.pk}/").status_code,
            401,
        )
        self.assertEqual(
            self.client.patch(f"/api/projects/{self.project.pk}/").status_code,
            401,
        )
        self.assertEqual(
            self.client.delete(f"/api/projects/{self.project.pk}/").status_code,
            401,
        )

    def test_list_only_returns_accessible_projects_and_search_is_case_insensitive(self):
        inaccessible = Project.objects.create(
            manager=self.outsider,
            title="Beta planning",
        )
        self.client.force_authenticate(self.member)

        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [project["projectId"] for project in response.json()],
            [self.project.pk],
        )

        response = self.client.get("/api/projects/?name=ALPHA")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [project["projectId"] for project in response.json()],
            [self.project.pk],
        )
        self.assertNotIn(inaccessible.pk, [p["projectId"] for p in response.json()])

    def test_create_uses_authenticated_manager_and_rejects_spoofed_owner(self):
        self.client.force_authenticate(self.manager)
        response = self.client.post(
            "/api/projects/",
            {"title": "New project", "managerId": self.outsider.pk},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Project.objects.filter(title="New project").exists())

        response = self.client.post(
            "/api/projects/",
            {"title": "  New project  ", "description": None},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "New project")
        self.assertEqual(response.json()["managerId"], self.manager.pk)
        self.assertEqual(response.json()["description"], "")
        self.assertIn("Location", response.headers)

    def test_non_project_manager_cannot_create_projects(self):
        for user in (self.member, self.admin):
            self.client.force_authenticate(user)
            response = self.client.post(
                "/api/projects/",
                {"title": "New project"},
                format="json",
            )
            self.assertEqual(response.status_code, 403)

    def test_title_and_description_limits_are_validated(self):
        self.client.force_authenticate(self.manager)
        invalid_payloads = (
            {"title": "ab"},
            {"title": "x" * 101},
            {"title": "Valid title", "description": "x" * 1001},
        )
        for payload in invalid_payloads:
            response = self.client.post(
                "/api/projects/",
                payload,
                format="json",
            )
            self.assertEqual(response.status_code, 400)

        response = self.client.get("/api/projects/?name=%20%20")
        self.assertEqual(response.status_code, 400)

    def test_patch_rejects_empty_payload_and_unknown_fields(self):
        self.client.force_authenticate(self.manager)
        url = f"/api/projects/{self.project.pk}/"

        empty_response = self.client.patch(url, {}, format="json")
        self.assertEqual(empty_response.status_code, 400)

        spoofed_response = self.client.patch(
            url,
            {"managerId": self.outsider.pk},
            format="json",
        )
        self.assertEqual(spoofed_response.status_code, 400)
        self.project.refresh_from_db()
        self.assertEqual(self.project.manager_id, self.manager.pk)

        invalid_title_response = self.client.patch(
            url,
            {"title": "ab"},
            format="json",
        )
        self.assertEqual(invalid_title_response.status_code, 400)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Alpha planning")

    def test_member_can_read_but_cannot_update_or_delete(self):
        self.client.force_authenticate(self.member)
        response = self.client.get(f"/api/projects/{self.project.pk}/")
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(
            f"/api/projects/{self.project.pk}/",
            {"title": "Changed title"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(f"/api/projects/{self.project.pk}/")
        self.assertEqual(response.status_code, 403)

    def test_inaccessible_and_missing_projects_return_not_found(self):
        self.client.force_authenticate(self.outsider)
        for project_id in (self.project.pk, 999999):
            self.assertEqual(
                self.client.get(f"/api/projects/{project_id}/").status_code,
                404,
            )
            self.assertEqual(
                self.client.patch(
                    f"/api/projects/{project_id}/",
                    {"title": "Changed title"},
                    format="json",
                ).status_code,
                404,
            )
            self.assertEqual(
                self.client.delete(f"/api/projects/{project_id}/").status_code,
                404,
            )

    def test_project_members_are_visible_to_accessible_users_and_only_active(self):
        inactive = User.objects.create_user(
            "inactive@example.test",
            "test-password",
            role=User.Role.DEVELOPER,
            is_active=False,
        )
        ProjectMember.objects.create(project=self.project, user=inactive)
        self.client.force_authenticate(self.member)

        response = self.client.get(f"/api/projects/{self.project.pk}/members/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {item["userId"] for item in response.json()},
            {self.manager.pk, self.member.pk},
        )
        self.assertTrue(
            all({"userId", "email", "role"} <= item.keys() for item in response.json())
        )

        self.client.force_authenticate(self.outsider)
        self.assertEqual(
            self.client.get(f"/api/projects/{self.project.pk}/members/").status_code,
            404,
        )

    def test_admin_can_read_all_project_data_but_cannot_change_it(self):
        task = Task.objects.create(project=self.project, title="Visible task")
        self.client.force_authenticate(self.admin)

        self.assertEqual(
            self.client.get("/api/projects/").json()[0]["projectId"],
            self.project.pk,
        )
        self.assertEqual(
            self.client.get(f"/api/projects/{self.project.pk}/").status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                f"/api/projects/{self.project.pk}/tasks/"
            ).json()[0]["taskId"],
            task.pk,
        )
        self.assertEqual(
            self.client.get(f"/api/projects/{self.project.pk}/members/").status_code,
            200,
        )

        self.assertEqual(
            self.client.patch(
                f"/api/projects/{self.project.pk}/",
                {"title": "Changed by Admin"},
                format="json",
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.delete(f"/api/projects/{self.project.pk}/").status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                f"/api/projects/{self.project.pk}/tasks/",
                {"title": "Admin task"},
                format="json",
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                f"/api/projects/{self.project.pk}/members/",
                {"userId": self.outsider.pk},
                format="json",
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(
                f"/api/projects/{self.project.pk}/eligible-members/"
            ).status_code,
            403,
        )

    def test_project_manager_can_add_and_remove_members_and_assignments(self):
        inactive = User.objects.create_user(
            "inactive@example.test",
            "test-password",
            role=User.Role.DEVELOPER,
            is_active=False,
        )
        task = Task.objects.create(project=self.project, title="Assigned task")
        members_url = f"/api/projects/{self.project.pk}/members/"
        eligible_url = f"/api/projects/{self.project.pk}/eligible-members/"
        self.client.force_authenticate(self.manager)

        eligible = self.client.get(eligible_url)
        self.assertEqual(eligible.status_code, 200)
        eligible_ids = {user["userId"] for user in eligible.json()}
        self.assertIn(self.admin.pk, eligible_ids)
        self.assertIn(self.outsider.pk, eligible_ids)
        self.assertNotIn(self.manager.pk, eligible_ids)
        self.assertNotIn(self.member.pk, eligible_ids)
        self.assertNotIn(inactive.pk, eligible_ids)

        added = self.client.post(
            members_url,
            {"userId": self.outsider.pk},
            format="json",
        )
        self.assertEqual(added.status_code, 201)
        self.assertEqual(added.json()["userId"], self.outsider.pk)
        self.assertEqual(
            self.client.post(
                members_url,
                {"userId": self.outsider.pk},
                format="json",
            ).status_code,
            409,
        )
        self.assertEqual(
            self.client.post(
                members_url,
                {"userId": self.manager.pk},
                format="json",
            ).status_code,
            409,
        )
        self.assertEqual(
            self.client.post(
                members_url,
                {"userId": inactive.pk},
                format="json",
            ).status_code,
            400,
        )

        TaskAssignee.objects.create(task=task, user=self.outsider)
        self.assertEqual(
            self.client.delete(
                f"{members_url}{self.outsider.pk}/"
            ).status_code,
            204,
        )
        self.assertFalse(
            ProjectMember.objects.filter(
                project=self.project,
                user=self.outsider,
            ).exists()
        )
        self.assertFalse(
            TaskAssignee.objects.filter(task=task, user=self.outsider).exists()
        )

        self.client.force_authenticate(self.outsider)
        self.assertEqual(
            self.client.get(f"/api/projects/{self.project.pk}/").status_code,
            404,
        )
        self.assertEqual(
            self.client.get(f"/api/projects/{self.project.pk}/tasks/").status_code,
            404,
        )

    def test_only_project_manager_can_manage_members(self):
        members_url = f"/api/projects/{self.project.pk}/members/"
        eligible_url = f"/api/projects/{self.project.pk}/eligible-members/"
        self.client.force_authenticate(self.member)

        self.assertEqual(self.client.get(eligible_url).status_code, 403)
        self.assertEqual(
            self.client.post(
                members_url,
                {"userId": self.outsider.pk},
                format="json",
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.delete(f"{members_url}{self.member.pk}/").status_code,
            403,
        )

    def test_manager_can_update_and_delete_with_cascade(self):
        task = Task.objects.create(project=self.project, title="Task")
        TaskAssignee.objects.create(task=task, user=self.member)
        Comment.objects.create(
            task=task,
            author=self.member,
            content="Comment",
        )
        project_id = self.project.pk
        task_id = task.pk
        self.client.force_authenticate(self.manager)

        response = self.client.patch(
            f"/api/projects/{project_id}/",
            {"title": "Updated title", "description": "Updated description"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated title")
        self.assertEqual(response.json()["description"], "Updated description")

        response = self.client.delete(f"/api/projects/{project_id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Project.objects.filter(pk=project_id).exists())
        self.assertFalse(Task.objects.filter(pk=task_id).exists())
        self.assertFalse(ProjectMember.objects.filter(project_id=project_id).exists())
        self.assertFalse(TaskAssignee.objects.filter(task_id=task_id).exists())
        self.assertFalse(Comment.objects.filter(task_id=task_id).exists())
