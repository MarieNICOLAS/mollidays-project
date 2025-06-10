from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from booking.models.booking import Booking
from rest_framework.response import Response
from circuits.models import Circuit

class BookingCancelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found or unauthorized"}, status=404)

        if booking.status == "cancelled":
            return Response({"error": "Already cancelled"}, status=400)

        booking.status = "cancelled"
        booking.is_validated = False
        booking.save()

        circuit = booking.circuit
        circuit.available_seats += booking.number_of_people
        circuit.save()

        return Response({"message": "Booking cancelled"})
