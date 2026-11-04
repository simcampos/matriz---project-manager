from django.test import TestCase
from rest_framework.test import APIClient

from apps.comments.models import Comment
from apps.accounts.models import User
from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task, TaskAssignee


class TaskDefaultsTests(TestCase):
    def test_status_and_priority_defaults(self):
        manager = User.objects.create_user(
            "pm@example.test",
            "test-password",
            role=User.Role.PROJECT_MANAGER,
        )
        project = Project.objects.create(manager=manager, title="Test project")
        task = Task.objects.create(project=project, title="Test task")

        self.assertEqual(task.status, Task.Status.TODO)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)


class TaskApiTests(TestCase):
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
        self.project = Project.objects.create(
            manager=self.manager,
            title="Task project",
        )
        ProjectMember.objects.create(project=self.project, user=self.member)
        self.base_url = f"/api/projects/{self.project.pk}/tasks/"

    def test_create_defaults_and_returns_a_retrievable_task(self):
        self.client.force_authenticate(self.manager)

        response = self.client.post(
            self.base_url,
            {"title": "  Initial task  ", "description": None},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        task_data = response.json()
        self.assertEqual(task_data["title"], "Initial task")
        self.assertEqual(task_data["description"], "")
        self.assertEqual(task_data["status"], Task.Status.TODO)
        self.assertEqual(task_data["priority"], Task.Priority.MEDIUM)
        self.assertEqual(task_data["assigneeIds"], [])
        self.assertIn("Location", response.headers)
        detail_response = self.client.get(
            f"{self.base_url}{task_data['taskId']}/"
        )
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json(), task_data)

    def test_title_and_description_constraints_are_validated(self):
        self.client.force_authenticate(self.manager)
        invalid_payloads = (
            {"title": ""},
            {"title": "   "},
            {"title": "ab"},
            {"title": "x" * 151},
            {"title": "Valid title", "description": "x" * 2001},
        )

        for payload in invalid_payloads:
            response = self.client.post(self.base_url, payload, format="json")
            self.assertEqual(response.status_code, 400, payload)

        self.assertFalse(Task.objects.exists())

    def test_invalid_status_or_priority_is_rejected_by_the_api(self):
        self.client.force_authenticate(self.manager)

        invalid_create = self.client.post(
            self.base_url,
            {"title": "Valid task", "status": "BLOCKED"},
            format="json",
        )
        self.assertEqual(invalid_create.status_code, 400)
        self.assertFalse(Task.objects.exists())

        task = Task.objects.create(project=self.project, title="Valid task")
        invalid_update = self.client.patch(
            f"{self.base_url}{task.pk}/",
            {"priority": "URGENT"},
            format="json",
        )
        self.assertEqual(invalid_update.status_code, 400)
        task.refresh_from_db()
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_list_filters_combine_and_invalid_filters_return_400(self):
        self.client.force_authenticate(self.manager)
        matching = Task.objects.create(
            project=self.project,
            title="Matching task",
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.HIGH,
        )
        other_status = Task.objects.create(
            project=self.project,
            title="Other status",
            status=Task.Status.TODO,
            priority=Task.Priority.HIGH,
        )
        TaskAssignee.objects.create(task=matching, user=self.member)

        response = self.client.get(
            self.base_url,
            {
                "status": "IN_PROGRESS",
                "priority": "HIGH",
                "assigneeId": self.member.pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["taskId"] for item in response.json()],
            [matching.pk],
        )

        invalid_status = self.client.get(self.base_url, {"status": "BLOCKED"})
        invalid_assignee = self.client.get(self.base_url, {"assigneeId": "0"})
        self.assertEqual(invalid_status.status_code, 400)
        self.assertEqual(invalid_assignee.status_code, 400)
        self.assertNotEqual(matching.pk, other_status.pk)

    def test_manager_can_update_and_delete_with_dependent_rows(self):
        self.client.force_authenticate(self.manager)
        task = Task.objects.create(project=self.project, title="Task to change")
        TaskAssignee.objects.create(task=task, user=self.member)
        Comment.objects.create(
            task=task,
            author=self.member,
            content="Related comment",
        )
        task_url = f"{self.base_url}{task.pk}/"

        response = self.client.patch(
            task_url,
            {
                "title": "Updated task",
                "description": "More detail",
                "status": "DONE",
                "priority": "LOW",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated task")
        self.assertEqual(response.json()["status"], Task.Status.DONE)
        self.assertEqual(response.json()["priority"], Task.Priority.LOW)

        delete_response = self.client.delete(task_url)
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
        self.assertFalse(TaskAssignee.objects.filter(task_id=task.pk).exists())
        self.assertFalse(Comment.objects.filter(task_id=task.pk).exists())

    def test_assigned_developer_can_only_update_task_status(self):
        task = Task.objects.create(project=self.project, title="Assigned task")
        TaskAssignee.objects.create(task=task, user=self.member)
        self.client.force_authenticate(self.member)
        task_url = f"{self.base_url}{task.pk}/"

        response = self.client.patch(
            task_url,
            {"status": "IN_PROGRESS"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        filtered_tasks = self.client.get(
            self.base_url,
            {"status": "IN_PROGRESS"},
        )
        self.assertEqual(filtered_tasks.status_code, 200)
        self.assertEqual(
            [item["taskId"] for item in filtered_tasks.json()],
            [task.pk],
        )
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)

        forbidden_update = self.client.patch(
            task_url,
            {"title": "Changed title"},
            format="json",
        )
        self.assertEqual(forbidden_update.status_code, 403)
        task.refresh_from_db()
        self.assertEqual(task.title, "Assigned task")

    def test_project_members_can_read_but_cannot_manage_tasks(self):
        task = Task.objects.create(project=self.project, title="Member task")
        self.client.force_authenticate(self.member)

        self.assertEqual(self.client.get(self.base_url).status_code, 200)
        self.assertEqual(
            self.client.get(f"{self.base_url}{task.pk}/").status_code,
            200,
        )
        self.assertEqual(
            self.client.post(
                self.base_url,
                {"title": "Another task"},
                format="json",
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.patch(
                f"{self.base_url}{task.pk}/",
                {"status": "DONE"},
                format="json",
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.delete(f"{self.base_url}{task.pk}/").status_code,
            403,
        )

    def test_inaccessible_project_tasks_are_not_revealed(self):
        task = Task.objects.create(project=self.project, title="Private task")
        self.client.force_authenticate(self.outsider)

        self.assertEqual(self.client.get(self.base_url).status_code, 404)
        self.assertEqual(
            self.client.get(f"{self.base_url}{task.pk}/").status_code,
            404,
        )
        self.assertEqual(
            self.client.post(
                self.base_url,
                {"title": "Unauthorized task"},
                format="json",
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.patch(
                f"{self.base_url}{task.pk}/",
                {"status": "DONE"},
                format="json",
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.delete(f"{self.base_url}{task.pk}/").status_code,
            404,
        )

    def test_task_data_is_persisted_and_available_on_subsequent_requests(self):
        self.client.force_authenticate(self.manager)
        created = self.client.post(
            self.base_url,
            {"title": "Persisted task"},
            format="json",
        )
        task_id = created.json()["taskId"]

        self.client.force_authenticate(self.member)
        listed = self.client.get(self.base_url)
        fetched = self.client.get(f"{self.base_url}{task_id}/")

        self.assertEqual(listed.status_code, 200)
        self.assertEqual(fetched.status_code, 200)
        self.assertEqual(fetched.json()["title"], "Persisted task")
        self.assertEqual([task["taskId"] for task in listed.json()], [task_id])


class TaskAssigneeApiTests(TestCase):
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
        self.other_member = User.objects.create_user(
            "other@example.test",
            "test-password",
            role=User.Role.DEVELOPER,
        )
        self.outsider = User.objects.create_user(
            "outsider@example.test",
            "test-password",
            role=User.Role.DEVELOPER,
        )
        self.inactive_member = User.objects.create_user(
            "inactive@example.test",
            "test-password",
            role=User.Role.DEVELOPER,
            is_active=False,
        )
        self.project = Project.objects.create(
            manager=self.manager,
            title="Assignment project",
        )
        ProjectMember.objects.create(project=self.project, user=self.member)
        ProjectMember.objects.create(project=self.project, user=self.other_member)
        ProjectMember.objects.create(
            project=self.project,
            user=self.inactive_member,
        )
        self.task = Task.objects.create(
            project=self.project,
            title="Assignment task",
        )
        self.assignees_url = (
            f"/api/projects/{self.project.pk}/tasks/{self.task.pk}/assignees/"
        )

    def test_manager_can_assign_and_list_users_and_duplicate_returns_409(self):
        self.client.force_authenticate(self.manager)

        response = self.client.post(
            self.assignees_url,
            {"userId": self.member.pk},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["userId"], self.member.pk)
        self.assertEqual(response.json()["email"], self.member.email)

        listed = self.client.get(self.assignees_url)
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(
            [item["userId"] for item in listed.json()],
            [self.member.pk],
        )

        duplicate = self.client.post(
            self.assignees_url,
            {"userId": self.member.pk},
            format="json",
        )
        self.assertEqual(duplicate.status_code, 409)
        self.assertEqual(self.task.assignees.count(), 1)

    def test_assignment_rejects_unknown_inactive_and_ineligible_users(self):
        self.client.force_authenticate(self.manager)
        for user_id in (999999, self.inactive_member.pk, self.outsider.pk):
            response = self.client.post(
                self.assignees_url,
                {"userId": user_id},
                format="json",
            )
            self.assertEqual(response.status_code, 400, user_id)
        self.assertEqual(self.task.assignees.count(), 0)

    def test_manager_can_remove_one_assignee_and_keep_the_others(self):
        self.task.assignees.add(self.member, self.other_member)
        self.client.force_authenticate(self.manager)

        response = self.client.delete(
            f"{self.assignees_url}{self.member.pk}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            list(self.task.assignees.values_list("pk", flat=True)),
            [self.other_member.pk],
        )

    def test_existing_put_contract_replaces_assignment_list(self):
        self.client.force_authenticate(self.manager)

        response = self.client.put(
            self.assignees_url,
            {"assigneeIds": [self.member.pk, self.other_member.pk]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {item["userId"] for item in response.json()},
            {self.member.pk, self.other_member.pk},
        )

        duplicate_ids = self.client.put(
            self.assignees_url,
            {"assigneeIds": [self.member.pk, self.member.pk]},
            format="json",
        )
        self.assertEqual(duplicate_ids.status_code, 400)
        self.assertEqual(self.task.assignees.count(), 2)

    def test_project_members_can_read_but_only_manager_can_change_assignments(self):
        self.client.force_authenticate(self.member)
        self.assertEqual(self.client.get(self.assignees_url).status_code, 200)
        self.assertEqual(
            self.client.post(
                self.assignees_url,
                {"userId": self.other_member.pk},
                format="json",
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.put(
                self.assignees_url,
                {"assigneeIds": [self.other_member.pk]},
                format="json",
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.delete(
                f"{self.assignees_url}{self.other_member.pk}/"
            ).status_code,
            403,
        )
        self.assertEqual(self.task.assignees.count(), 0)

    def test_inaccessible_user_cannot_read_or_change_assignments(self):
        self.client.force_authenticate(self.outsider)
        self.assertEqual(self.client.get(self.assignees_url).status_code, 404)
        self.assertEqual(
            self.client.post(
                self.assignees_url,
                {"userId": self.member.pk},
                format="json",
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.delete(
                f"{self.assignees_url}{self.member.pk}/"
            ).status_code,
            404,
        )
        self.assertEqual(self.task.assignees.count(), 0)
