from rest_framework import serializers
from django.utils import timezone
import re

class NextTrackingNumberSerializer(serializers.Serializer):
    origin_country_id = serializers.RegexField(
        regex=r'^[A-Z]{2}$',
        max_length=2,
        min_length=2,
        error_messages={'invalid': 'Invalid origin country code format.'}
    )
    destination_country_id = serializers.RegexField(
        regex=r'^[A-Z]{2}$',
        max_length=2,
        min_length=2,
        error_messages={'invalid': 'Invalid destination country code format.'}
    )
    weight = serializers.DecimalField(
        max_digits=6, 
        decimal_places=3, 
        min_value=0.001, 
        max_value=1000,  # Added max_value constraint directly
        error_messages={'max_value': 'Weight exceeds the maximum allowed limit.'}
    )
    created_at = serializers.DateTimeField()
    customer_id = serializers.UUIDField()
    customer_name = serializers.CharField(max_length=100)
    customer_slug = serializers.RegexField(
        regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$', 
        max_length=100,
        error_messages={'invalid': 'Enter a valid slug format.'}
    )

    def validate_created_at(self, value):
        """ Ensure the 'created_at' field is not in the future. """
        if value > timezone.now():
            raise serializers.ValidationError("The creation timestamp cannot be in the future.")
        return value
