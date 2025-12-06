from rest_framework import serializers

from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = "__all__"
        read_only_fields = ["realtor", "created_at"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive integer.")
        return value

    def validate_bedrooms(self, value):
        if value < 0:
            raise serializers.ValidationError("Bedrooms must be a positive integer.")
        return value

    def validate_bathrooms(self, value):
        if value <= 0 or value >= 10:
            return 1.0
        return round(float(value), 1)

    def to_internal_value(self, data):
        # Make a mutable copy if needed
        if hasattr(data, "copy"):
            data = data.copy()

        # Handle string boolean conversion for is_published
        if "is_published" in data and isinstance(data["is_published"], str):
            data["is_published"] = data["is_published"] == "True"

        # Handle sale_type conversion
        if "sale_type" in data:
            sale_type_map = {"FOR_RENT": "For Rent", "FOR_SALE": "For Sale"}
            data["sale_type"] = sale_type_map.get(data["sale_type"], data["sale_type"])

        # Handle home_type conversion
        if "home_type" in data:
            home_type_map = {
                "TOWNHOUSE": "Townhouse",
                "CONDO": "Condo",
                "HOUSE": "House",
            }
            data["home_type"] = home_type_map.get(data["home_type"], data["home_type"])

        return super().to_internal_value(data)
