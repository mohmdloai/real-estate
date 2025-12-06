from django.conf import settings

import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token


class GoogleAuthError(Exception):
    """Custom exception for Google authentication errors."""

    pass


class GoogleAuthService:
    """Service for handling Google OAuth authentication."""

    GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    @staticmethod
    def verify_id_token(token: str) -> dict:
        """
        Verify Google ID token and return user info.

        Args:
            token: Google ID token from frontend

        Returns:
            dict with user info (email, name, picture, etc.)

        Raises:
            GoogleAuthError: If token is invalid
        """
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )

            # Verify issuer
            if idinfo["iss"] not in [
                "accounts.google.com",
                "https://accounts.google.com",
            ]:
                raise GoogleAuthError("Invalid token issuer")

            # Verify email is verified
            if not idinfo.get("email_verified", False):
                raise GoogleAuthError("Email not verified by Google")

            return {
                "email": idinfo["email"],
                "name": idinfo.get("name", ""),
                "picture": idinfo.get("picture", ""),
                "google_id": idinfo["sub"],
            }

        except ValueError as e:
            raise GoogleAuthError(f"Invalid token: {str(e)}")

    @staticmethod
    def verify_access_token(access_token: str) -> dict:
        """
        Verify Google access token and fetch user info.

        Args:
            access_token: Google access token from frontend

        Returns:
            dict with user info

        Raises:
            GoogleAuthError: If token is invalid
        """
        try:
            # Verify token
            token_response = requests.get(
                GoogleAuthService.GOOGLE_TOKEN_INFO_URL,
                params={"access_token": access_token},
                timeout=10,
            )

            if token_response.status_code != 200:
                raise GoogleAuthError("Invalid access token")

            token_info = token_response.json()

            # Verify the token belongs to our app
            if token_info.get("aud") != settings.GOOGLE_CLIENT_ID:
                raise GoogleAuthError("Token was not issued for this application")

            # Fetch user info
            user_response = requests.get(
                GoogleAuthService.GOOGLE_USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            )

            if user_response.status_code != 200:
                raise GoogleAuthError("Failed to fetch user info")

            user_info = user_response.json()

            return {
                "email": user_info["email"],
                "name": user_info.get("name", ""),
                "picture": user_info.get("picture", ""),
                "google_id": user_info["sub"],
            }

        except requests.RequestException as e:
            raise GoogleAuthError(f"Network error: {str(e)}")
