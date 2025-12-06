from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import (
    GoogleAuthResponseSerializer,
    GoogleAuthSerializer,
    RegisterSerializer,
    UserSerializer,
    get_tokens_for_user,
)
from .services.google_auth import GoogleAuthError, GoogleAuthService

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST: Register a new user or realtor.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data
        validated_data = serializer.validated_data
        is_realtor = validated_data.pop("is_realtor", False)
        password = validated_data.pop("password")

        # Create user based on type
        if is_realtor:
            user = User.objects.create_realtor(
                password=password,
                auth_provider="email",
                **validated_data,
            )
            message = "Realtor created successfully"
        else:
            user = User.objects.create_user(
                password=password,
                auth_provider="email",
                **validated_data,
            )
            message = "User created successfully"

        return Response(
            {"success": message, "email": user.email},
            status=status.HTTP_201_CREATED,
        )


class RetrieveUserView(generics.RetrieveAPIView):
    """
    GET: Retrieve authenticated user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class GoogleAuthView(generics.GenericAPIView):
    """
    POST: Handle Google OAuth authentication.

    Supports both sign-in and registration:
    - If user exists: Sign in and return tokens
    - If user doesn't exist: Create account and return tokens
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        token_type = serializer.validated_data["token_type"]
        is_realtor = serializer.validated_data["is_realtor"]

        try:
            # Verify Google token
            if token_type == "id_token":
                google_user_info = GoogleAuthService.verify_id_token(token)
            else:
                google_user_info = GoogleAuthService.verify_access_token(token)

            email = google_user_info["email"]
            name = google_user_info["name"]
            google_id = google_user_info["google_id"]
            picture = google_user_info.get("picture", "")

            # Check if user exists
            user = User.objects.filter(email=email).first()
            is_new_user = False

            if user:
                # Existing user - update Google info if needed
                if not user.google_id:
                    user.google_id = google_id
                    user.auth_provider = "google"

                if picture and not user.picture:
                    user.picture = picture

                user.save()
            else:
                # New user - create account
                is_new_user = True

                if is_realtor:
                    user = User.objects.create_realtor(
                        email=email,
                        name=name,
                        google_id=google_id,
                        picture=picture,
                        auth_provider="google",
                    )
                else:
                    user = User.objects.create_user(
                        email=email,
                        name=name,
                        google_id=google_id,
                        picture=picture,
                        auth_provider="google",
                    )

            # Generate JWT tokens
            tokens = get_tokens_for_user(user)

            response_data = {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "user": UserSerializer(user).data,
                "is_new_user": is_new_user,
            }

            response_serializer = GoogleAuthResponseSerializer(data=response_data)
            response_serializer.is_valid()

            return Response(
                response_data,
                status=status.HTTP_201_CREATED if is_new_user else status.HTTP_200_OK,
            )

        except GoogleAuthError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            return Response(
                {"error": "Authentication failed. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GoogleAuthCallbackView(generics.GenericAPIView):
    """
    GET: Handle OAuth callback from Google (for server-side flow).
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        """Handle the OAuth callback redirect."""
        code = request.query_params.get("code")
        error = request.query_params.get("error")

        if error:
            return Response(
                {"error": f"Google authentication failed: {error}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not code:
            return Response(
                {"error": "No authorization code provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Return the code to be exchanged on frontend
        return Response(
            {
                "code": code,
                "message": "Exchange this code for tokens using the token endpoint",
            },
            status=status.HTTP_200_OK,
        )