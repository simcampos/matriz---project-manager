from collections.abc import Mapping

from rest_framework import serializers

from apps.comments.models import Comment
from apps.projects.serializers import ProjectMemberUserSerializer


class StrictSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        if isinstance(data, Mapping):
            unknown_fields = set(data) - set(self.fields)
            if unknown_fields:
                raise serializers.ValidationError(
                    {
                        field: ["Unknown field."]
                        for field in sorted(unknown_fields)
                    }
                )
        return super().to_internal_value(data)


class CommentCreateSerializer(StrictSerializer):
    content = serializers.CharField(
        min_length=1,
        max_length=2000,
        trim_whitespace=False,
    )

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Comment content cannot contain only whitespace."
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    commentId = serializers.IntegerField(source="pk", read_only=True)
    taskId = serializers.IntegerField(source="task_id", read_only=True)
    author = ProjectMemberUserSerializer(read_only=True)
    createdAt = serializers.DateTimeField(
        source="created_at",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ["commentId", "taskId", "author", "content", "createdAt"]
