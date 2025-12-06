from django.urls import path

from .views import (
    PublicListingDetailView,
    PublicListingListView,
    RealtorListingDetailView,
    RealtorListingListCreateView,
)

urlpatterns = [
    # Realtor endpoints (authenticated)
    path("manage/", RealtorListingListCreateView.as_view(), name="listing-manage"),
    path(
        "manage/<slug:slug>/",
        RealtorListingDetailView.as_view(),
        name="listing-manage-detail",
    ),
    # Public endpoints
    path("", PublicListingListView.as_view(), name="listing-list"),
    path("<slug:slug>/", PublicListingDetailView.as_view(), name="listing-detail"),
]