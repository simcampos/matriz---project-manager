from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comments.models import Comment
from apps.comments.serializers import CommentCreateSerializer, CommentSerializer
from apps.tasks.views import get_project_task


class ProjectTaskCommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, task_id):
        task = get_project_task(request.user, project_id, task_id)
        comments = task.comments.select_related("author").order_by(
            "created_at",
            "id",
        )
        return Response(CommentSerializer(comments, many=True).data)

    def post(self, request, project_id, task_id):
        task = get_project_task(request.user, project_id, task_id)
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = Comment.objects.create(
            task=task,
            author=request.user,
            content=serializer.validated_data["content"],
        )
        return Response(
            CommentSerializer(comment).data,
            status=201,
        )
