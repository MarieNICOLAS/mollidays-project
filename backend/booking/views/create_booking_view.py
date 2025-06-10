from rest_framework import generics, permissions
from booking.models.booking import Booking
from booking.serializers.booking_serializer import BookingSerializer
from circuits.models import Circuit
from rest_framework.response import Response
from rest_framework import status



class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        circuit_id = request.data.get('circuit_id')
        number_of_people = int(request.data.get('number_of_people', 1))

        try:
            circuit = Circuit.objects.get(id=circuit_id)
        except Circuit.DoesNotExist:
            return Response({"error": "Circuit not found"}, status=status.HTTP_404_NOT_FOUND)

        if circuit.available_seats < number_of_people:
            return Response({"error": "Not enough seats available"}, status=status.HTTP_400_BAD_REQUEST)

        # Calcul du total
        total = circuit.price * number_of_people

        # Réduction des places
        circuit.available_seats -= number_of_people
        circuit.save()


        booking = Booking.objects.create(
            user=user,
            circuit=circuit,
            number_of_people=number_of_people,
            total_amount=total,
            start_date=circuit.start_date,
            end_date=circuit.end_date,
        )

        return Response({
            "message": "Booking successful!",
            "booking_id": booking.id
        }, status=status.HTTP_201_CREATED)
