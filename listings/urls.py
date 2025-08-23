from django.urls import path
from .views import ManagingListingView

urlpatterns = [
    path('create' , ManagingListingView.as_view())
]