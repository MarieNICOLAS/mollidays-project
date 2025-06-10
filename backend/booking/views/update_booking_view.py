from rest_framework import generics, permissions
from booking.models.booking import Booking
from booking.serializers.booking_serializer import BookingSerializer

class BookingUpdateAPIView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
