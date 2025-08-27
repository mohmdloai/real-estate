from django.urls import path
from .views import ManagingListingView, ListingDetailView, ListingView

urlpatterns = [
    path('manage' , ManagingListingView.as_view()),
    path('detail' , ListingDetailView .as_view()),
    path('get-listings' , ListingView .as_view()),
]