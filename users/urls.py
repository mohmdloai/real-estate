from django.urls import path
from .views import RegisterView, RetrieveUserView


urlpatterns= [
    path('register', RegisterView.as_view(), name='user-register'),
    path('me', RetrieveUserView.as_view(), name='user-retrieve'),
]