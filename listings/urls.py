from django.urls import path
from .views import ManagingListingView, ListingDetailView

urlpatterns = [
    path('manage' , ManagingListingView.as_view()),
    path('detail' , ListingDetailView .as_view()),
]