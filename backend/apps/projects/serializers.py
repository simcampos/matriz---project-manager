from rest_framework import serializers

from apps.accounts.models import User
from apps.common.serializers import StrictSerializer
from apps.projects.models import Project


class ProjectWriteFields(StrictSerializer):
    title = serializers.CharField(
        min_length=3,
        max_length=100,
        trim_whitespace=True,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=1000,
        trim_whitespace=False,
    )

    def validate_description(self, value):
        return value or ""


class ProjectCreateSerializer(ProjectWriteFields):
    pass


class ProjectUpdateSerializer(ProjectWriteFields):
    title = serializers.CharField(
        required=False,
        min_length=3,
        max_length=100,
        trim_whitespace=True,
    )

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "At least one project field must be provided."
            )
        return attrs


class ProjectSerializer(serializers.ModelSerializer):
    projectId = serializers.IntegerField(source="pk", read_only=True)
    managerId = serializers.IntegerField(source="manager_id", read_only=True)

    class Meta:
        model = Project
        fields = ["projectId", "managerId", "title", "description"]


class ProjectMemberUserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = User
        fields = ["userId", "email", "role"]


class ProjectMemberCreateSerializer(StrictSerializer):
    userId = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.filter(is_active=True),
    )
