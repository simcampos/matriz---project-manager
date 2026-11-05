from rest_framework import serializers

from apps.accounts.models import User
from apps.common.serializers import StrictSerializer


class UserRoleUpdateSerializer(StrictSerializer):
    role = serializers.ChoiceField(choices=User.Role.choices)
