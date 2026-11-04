from django.contrib.auth import authenticate, login, logout
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


class CurrentSessionDeleteView(APIView):
    authentication_classes = [SessionAuthentication401]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        logout(request._request)
        return Response(status=status.HTTP_204_NO_CONTENT)
