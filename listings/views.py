from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Listing
from .serializers import ListingSerializer


class IsRealtorPermission(permissions.BasePermission):
    """Custom permission to only allow realtors to access."""

    message = "User has no permission to access"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_realtor


class RealtorListingListCreateView(generics.ListCreateAPIView):
    """
    GET: List all listings for the authenticated realtor.
    POST: Create a new listing for the authenticated realtor.
    """

    serializer_class = ListingSerializer
    permission_classes = [IsRealtorPermission]

    def get_queryset(self):
        return Listing.objects.filter(
            realtor=self.request.user.email
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(realtor=self.request.user.email)

    def create(self, request, *args, **kwargs):
        slug = request.data.get("slug")
        if slug and Listing.objects.filter(slug=slug).exists():
            return Response(
                {"error": "Listing with this slug already exists!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)


class RealtorListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific listing by slug.
    PUT: Full update of a listing.
    PATCH: Partial update of a listing.
    DELETE: Delete a listing.
    """

    serializer_class = ListingSerializer
    permission_classes = [IsRealtorPermission]
    lookup_field = "slug"

    def get_queryset(self):
        return Listing.objects.filter(realtor=self.request.user.email)


class PublicListingListView(generics.ListAPIView):
    """
    GET: List all published listings (public access).
    """

    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Listing.objects.filter(is_published=True).order_by("-created_at")


class PublicListingDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a specific published listing by slug (public access).
    """

    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Listing.objects.filter(is_published=True)
