from rest_framework import serializers

from apps.common.serializers import StrictSerializer
from apps.comments.models import Comment
from apps.projects.serializers import ProjectMemberUserSerializer


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
