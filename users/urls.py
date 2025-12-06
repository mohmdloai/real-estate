from django.urls import path

from .views import (
    GoogleAuthCallbackView,
    GoogleAuthView,
    RegisterView,
    RetrieveUserView,
)

urlpatterns = [
    path("register", RegisterView.as_view(), name="user-register"),
    path("me", RetrieveUserView.as_view(), name="user-retrieve"),
    path("google/", GoogleAuthView.as_view(), name="google-auth"),
    path("google/callback/", GoogleAuthCallbackView.as_view(), name="google-callback"),
]