from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("name", "email", "is_realtor", "picture", "auth_provider")


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer for Google OAuth authentication."""

    token = serializers.CharField(required=True, help_text="Google ID or access token")
    token_type = serializers.ChoiceField(
        choices=["id_token", "access_token"],
        default="id_token",
        help_text="Type of Google token",
    )
    is_realtor = serializers.BooleanField(
        default=False,
        help_text="Register as realtor (only for new users)",
    )


class GoogleAuthResponseSerializer(serializers.Serializer):
    """Serializer for Google OAuth response."""

    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
    is_new_user = serializers.BooleanField()


def get_tokens_for_user(user):
    """Generate JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }