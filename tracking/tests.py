from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import TrackingNumber
from uuid import uuid4
from datetime import datetime
from django.utils import timezone

class NextTrackingNumberViewTests(APITestCase):
    def setUp(self):
        # This method is called before each test
        self.url = reverse('next_tracking_number')

    def test_generate_tracking_number_success(self):
        """Test that a tracking number is generated successfully."""
        response = self.client.get(self.url, {
            'origin_country_id': 'US',
            'destination_country_id': 'CA',
            'weight': '1.234',
            'created_at': timezone.now().isoformat(),
            'customer_id': str(uuid4()),
            'customer_name': 'Test Customer',
            'customer_slug': 'test-customer'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tracking_number', response.data)
        self.assertIn('created_at', response.data)
        self.assertEqual(len(response.data['tracking_number']), 16)

    def test_generate_tracking_number_invalid_country(self):
        """Test that an invalid country code returns a validation error."""
        response = self.client.get(self.url, {
            'origin_country_id': 'XX',  # Invalid country code
            'destination_country_id': 'YY',  # Invalid country code
            'weight': '1.234',
            'created_at': timezone.now().isoformat(),
            'customer_id': str(uuid4()),
            'customer_name': 'Test Customer',
            'customer_slug': 'test-customer'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('origin_country_id', response.data)
        self.assertIn('destination_country_id', response.data)

    def test_generate_tracking_number_missing_parameters(self):
        """Test that missing parameters return a validation error."""
        response = self.client.get(self.url, {
            'origin_country_id': 'US',
            # Missing destination_country_id
            'weight': '1.234',
            'created_at': timezone.now().isoformat(),
            'customer_id': str(uuid4()),
            'customer_name': 'Test Customer',
            'customer_slug': 'test-customer'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('destination_country_id', response.data)

    def test_generate_tracking_number_future_date(self):
        """Test that a future creation date returns a validation error."""
        future_date = (timezone.now() + timezone.timedelta(days=1)).isoformat()
        
        response = self.client.get(self.url, {
            'origin_country_id': 'US',
            'destination_country_id': 'CA',
            'weight': '1.234',
            'created_at': future_date,  # Future date
            'customer_id': str(uuid4()),
            'customer_name': 'Test Customer',
            'customer_slug': 'test-customer'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('created_at', response.data)
