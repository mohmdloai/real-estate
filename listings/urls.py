from django.urls import path
from .views import ManagingListingView

urlpatterns = [
    path('manage' , ManagingListingView.as_view())
]