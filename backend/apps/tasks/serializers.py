from rest_framework import serializers

from apps.accounts.models import User
from apps.common.serializers import StrictSerializer
from apps.tasks.models import Task


class TaskWriteFields(StrictSerializer):
    title = serializers.CharField(
        min_length=3,
        max_length=150,
        trim_whitespace=True,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=2000,
        trim_whitespace=False,
    )
    status = serializers.ChoiceField(
        choices=Task.Status.choices,
        required=False,
    )
    priority = serializers.ChoiceField(
        choices=Task.Priority.choices,
        required=False,
    )

    def validate_description(self, value):
        return value or ""


class TaskCreateSerializer(TaskWriteFields):
    status = serializers.ChoiceField(
        choices=Task.Status.choices,
        required=False,
        default=Task.Status.TODO,
    )
    priority = serializers.ChoiceField(
        choices=Task.Priority.choices,
        required=False,
        default=Task.Priority.MEDIUM,
    )


class TaskUpdateSerializer(TaskWriteFields):
    title = serializers.CharField(
        required=False,
        min_length=3,
        max_length=150,
        trim_whitespace=True,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=2000,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "At least one task field must be provided."
            )
        return attrs


class TaskFilterSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=Task.Status.choices,
        required=False,
    )
    priority = serializers.ChoiceField(
        choices=Task.Priority.choices,
        required=False,
    )
    assigneeId = serializers.IntegerField(
        source="assignee_id",
        required=False,
        min_value=1,
    )


class TaskAssigneeCreateSerializer(StrictSerializer):
    userId = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
    )


class TaskAssigneesUpdateSerializer(StrictSerializer):
    assigneeIds = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
    )

    def validate_assigneeIds(self, value):
        if len(set(value)) != len(value):
            raise serializers.ValidationError(
                "Assignee identifiers must be unique."
            )
        return value


class TaskSerializer(serializers.ModelSerializer):
    taskId = serializers.IntegerField(source="pk", read_only=True)
    projectId = serializers.IntegerField(source="project_id", read_only=True)
    assigneeIds = serializers.PrimaryKeyRelatedField(
        source="assignees",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Task
        fields = [
            "taskId",
            "projectId",
            "assigneeIds",
            "title",
            "description",
            "status",
            "priority",
        ]
