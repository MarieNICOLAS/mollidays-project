from rest_framework import viewsets, permissions
from booking.models.booking import Booking
from booking.serializers.booking_serializer import BookingSerializer


class AdminBookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAdminUser]