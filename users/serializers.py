from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "is_realtor", "picture", "auth_provider")


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration."""

    name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={"input_type": "password"},
    )
    re_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    is_realtor = serializers.BooleanField(default=False, required=False)

    def validate_email(self, value):
        """Check if email already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists!")
        return value

    def validate(self, data):
        """Validate password matching."""
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError(
                {"password": "Passwords don't match, please retry again"}
            )
        # Remove re_password from validated data
        data.pop("re_password")
        return data


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