from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from booking.models.booking import Booking
from booking.serializers.booking_serializer import BookingSerializer

class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
