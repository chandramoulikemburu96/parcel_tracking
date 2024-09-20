from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializations import NextTrackingNumberSerializer
from .models import TrackingNumber
import uuid
import datetime

class NextTrackingNumberView(APIView):
    def get(self, request):
        # Validate query parameters using the serializer
        serializer = NextTrackingNumberSerializer(data=request.query_params)
        if serializer.is_valid():
            # Generate a unique tracking number
            while True:
                tracking_number = str(uuid.uuid4()).replace("-", "").upper()[:16]
                
                # Check if the tracking number already exists
                if not TrackingNumber.objects.filter(tracking_number=tracking_number).exists():
                    break

            # Save the tracking number to the database
            tracking_number_instance = TrackingNumber.objects.create(
                tracking_number=tracking_number
            )

            # Create response data
            response_data = {
                'tracking_number': tracking_number_instance.tracking_number,
                'created_at': tracking_number_instance.created_at.isoformat(),
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # If validation fails, return error response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

