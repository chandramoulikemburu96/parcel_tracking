from rest_framework import serializers
import re
from uuid import UUID
from datetime import datetime
from django.utils import timezone
# from django_countries import countries  # Use django-countries for country code validation

class NextTrackingNumberSerializer(serializers.Serializer):
    origin_country_id = serializers.CharField(max_length=2, min_length=2)
    destination_country_id = serializers.CharField(max_length=2, min_length=2)
    weight = serializers.DecimalField(max_digits=6, decimal_places=3, min_value=0.001)
    created_at = serializers.DateTimeField()
    customer_id = serializers.UUIDField()
    customer_name = serializers.CharField(max_length=100)
    customer_slug = serializers.RegexField(
        regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$', 
        max_length=100,
        error_messages={'invalid': 'Enter a valid slug format.'}
    )

    def validate_origin_country_id(self, value):
        """ Validate that the origin country code is in ISO 3166-1 alpha-2 format and exists. """
        if not re.match(r'^[A-Z]{2}$', value):
            raise serializers.ValidationError("Invalid origin country code format.")
        # if value not in dict(countries):
        #     raise serializers.ValidationError("Origin country code is not a valid ISO 3166-1 alpha-2 code.")
        return value

    def validate_destination_country_id(self, value):
        """ Validate that the destination country code is in ISO 3166-1 alpha-2 format and exists. """
        if not re.match(r'^[A-Z]{2}$', value):
            raise serializers.ValidationError("Invalid destination country code format.")
        # if value not in dict(countries):
        #     raise serializers.ValidationError("Destination country code is not a valid ISO 3166-1 alpha-2 code.")
        return value


    def validate_weight(self, value):
        """ Additional weight validation if needed. """
        if value > 1000:  # Example constraint, change as needed
            raise serializers.ValidationError("Weight exceeds the maximum allowed limit.")
        return value

    def validate_customer_id(self, value):
        """ Custom validation for UUID. """
        try:
            UUID(str(value))
        except ValueError:
            raise serializers.ValidationError("Invalid UUID format for customer ID.")
        return value
    
    def validate_created_at(self, value):
        """ Ensure the 'created_at' field is not in the future. """
        # Use Django's timezone-aware current time
        now = timezone.now()

        # Check if the 'created_at' is in the future
        if value > now:
            raise serializers.ValidationError("The creation timestamp cannot be in the future.")
        return value
