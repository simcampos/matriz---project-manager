import os

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.accounts.models import User
from apps.projects.models import Project, ProjectMember
from apps.tasks.models import Task, TaskAssignee


USER_SPECS = (
    {
        "email": "admin@matriz.dev",
        "password_env": "DEMO_ADMIN_PASSWORD",
        "first_name": "Matriz",
        "last_name": "Admin",
        "role": User.Role.ADMIN,
        "is_staff": True,
    },
    {
        "email": "pm@matriz.dev",
        "password_env": "DEMO_PM_PASSWORD",
        "first_name": "Project",
        "last_name": "Manager",
        "role": User.Role.PROJECT_MANAGER,
    },
    {
        "email": "developer@matriz.dev",
        "password_env": "DEMO_DEVELOPER_PASSWORD",
        "first_name": "Demo",
        "last_name": "Developer",
        "role": User.Role.DEVELOPER,
    },
)


class Command(BaseCommand):
    help = "Create reproducible local demo users, projects, tasks, memberships, and assignments."

    @transaction.atomic
    def handle(self, *args, **options):
        passwords = {}
        missing_passwords = []
        for spec in USER_SPECS:
            if not User.objects.filter(email=spec["email"]).exists():
                password = os.environ.get(spec["password_env"])
                if not password:
                    missing_passwords.append(spec["password_env"])
                passwords[spec["email"]] = password

        if missing_passwords:
            names = ", ".join(missing_passwords)
            raise CommandError(f"Set these demo password variables in .env: {names}")

        users = {}
        created_users = 0
        for spec in USER_SPECS:
            email = spec["email"]
            defaults = {
                key: value
                for key, value in spec.items()
                if key not in {"email", "password_env"}
            }
            if email in passwords:
                defaults["password"] = make_password(passwords[email])

            user, created = User.objects.get_or_create(email=email, defaults=defaults)
            users[email] = user
            created_users += int(created)

        project_specs = (
            ("Planeamento de demonstração", "Projeto de exemplo para planear trabalho."),
            ("Entrega de demonstração", "Projeto de exemplo com trabalho em vários estados."),
        )
        projects = []
        created_projects = 0
        for title, description in project_specs:
            project, created = Project.objects.get_or_create(
                manager=users["pm@matriz.dev"],
                title=title,
                defaults={"description": description},
            )
            projects.append(project)
            created_projects += int(created)

        task_specs = (
            (
                projects[0],
                "Preparar plano",
                Task.Status.TODO,
                Task.Priority.MEDIUM,
            ),
            (
                projects[0],
                "Rever requisitos",
                Task.Status.IN_PROGRESS,
                Task.Priority.HIGH,
            ),
            (
                projects[1],
                "Entregar primeira versão",
                Task.Status.DONE,
                Task.Priority.LOW,
            ),
            (
                projects[1],
                "Validar demonstração",
                Task.Status.TODO,
                Task.Priority.MEDIUM,
            ),
        )
        tasks = []
        created_tasks = 0
        for project, title, status, priority in task_specs:
            task, created = Task.objects.get_or_create(
                project=project,
                title=title,
                defaults={"status": status, "priority": priority},
            )
            tasks.append(task)
            created_tasks += int(created)

        created_memberships = 0
        for project in projects:
            _, created = ProjectMember.objects.get_or_create(
                project=project,
                user=users["developer@matriz.dev"],
            )
            created_memberships += int(created)

        created_assignees = 0
        for task in tasks:
            if task.status != Task.Status.DONE:
                _, created = TaskAssignee.objects.get_or_create(
                    task=task,
                    user=users["developer@matriz.dev"],
                )
                created_assignees += int(created)

        self.stdout.write(
            self.style.SUCCESS(
                "Demo seed complete "
                f"(created users={created_users}, projects={created_projects}, "
                f"tasks={created_tasks}, memberships={created_memberships}, "
                f"assignees={created_assignees})."
            )
        )
