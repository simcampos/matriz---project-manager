from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import serializers, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import SessionAuthentication401
from apps.accounts.models import User
from apps.accounts.permissions import IsAdmin
from apps.accounts.serializers import UserRoleUpdateSerializer


class SessionCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)


def serialize_user(user):
    return {
        "userId": user.pk,
        "email": user.email,
        "role": user.role,
        "isActive": user.is_active,
    }


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def csrf_cookie(request):
    return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_protect, name="dispatch")
class SessionCreateView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SessionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()
        user = authenticate(
            request=request._request,
            email=email,
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {
                    "code": "invalid_credentials",
                    "message": "Email ou palavra-passe inválidos.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request._request, user)
        return Response(
            {"user": serialize_user(user)},
            status=status.HTTP_200_OK,
        )


class CurrentUserView(APIView):
    authentication_classes = [SessionAuthentication401]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(serialize_user(request.user))


class UserListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.all()
        return Response([serialize_user(user) for user in users])


class UserRoleUpdateView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, user_id):
        serializer = UserRoleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_role = serializer.validated_data["role"]

        with transaction.atomic():
            active_admins = list(
                User.objects.select_for_update()
                .filter(role=User.Role.ADMIN, is_active=True)
                .order_by("pk")
            )
            user = get_object_or_404(
                User.objects.select_for_update(),
                pk=user_id,
            )

            if (
                user.is_active
                and user.role == User.Role.ADMIN
                and new_role != User.Role.ADMIN
                and len(active_admins) <= 1
            ):
                return Response(
                    {"detail": "The last active Admin cannot be demoted."},
                    status=status.HTTP_409_CONFLICT,
                )

            if (
                user.role == User.Role.PROJECT_MANAGER
                and new_role != User.Role.PROJECT_MANAGER
                and user.managed_projects.exists()
            ):
                return Response(
                    {
                        "detail": (
                            "A Project Manager who manages projects cannot "
                            "be demoted."
                        )
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            user.role = new_role
            user.save(update_fields=["role"])

        return Response(serialize_user(user))


class CurrentSessionDeleteView(APIView):
    authentication_classes = [SessionAuthentication401]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        logout(request._request)
        return Response(status=status.HTTP_204_NO_CONTENT)
