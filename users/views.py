from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    GoogleAuthResponseSerializer,
    GoogleAuthSerializer,
    UserSerializer,
    get_tokens_for_user,
)
from .services.google_auth import GoogleAuthError, GoogleAuthService

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            data = request.data

            name = data["name"]
            email = data["email"]
            password = data["password"]
            re_password = data["re_password"]
            is_realtor = data.get("is_realtor", "False")

            if is_realtor == "True":
                is_realtor = True
            else:
                is_realtor = False

            if password != re_password:
                return Response(
                    {"error": "Password don't match, Please retry again"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if len(password) < 8:
                return Response(
                    {"error": "Password must be at least 8 characters!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "User already exists!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if is_realtor:
                User.objects.create_realtor(
                    name=name,
                    email=email,
                    password=password,
                    auth_provider="email",
                )
                return Response(
                    {"success": "Realtor created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                User.objects.create_user(
                    name=name,
                    email=email,
                    password=password,
                    auth_provider="email",
                )
                return Response(
                    {"success": "User created successfully", "email": email},
                    status=status.HTTP_201_CREATED,
                )

        except KeyError as e:
            return Response(
                {"error": f"Missing required field: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"error": "Oh!, something went wrong while registering"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetrieveUserView(APIView):

    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)
            return Response({"user": user.data}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Oh!, something went wrong while retrieving data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GoogleAuthView(APIView):
    """
    Handle Google OAuth authentication.

    Supports both sign-in and registration:
    - If user exists: Sign in and return tokens
    - If user doesn't exist: Create account and return tokens
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        except Exception:
            return Response(
                {"error": "Authentication failed. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GoogleAuthCallbackView(APIView):
    """
    Handle OAuth callback from Google (for server-side flow).
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
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