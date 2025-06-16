from rest_framework import generics, permissions
from rest_framework.response import Response
from booking.models.booking import Booking
from booking.serializers.booking_serializer import BookingSerializer

class BookingUpdateAPIView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        old_number = instance.number_of_people
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        new_number = serializer.validated_data.get("number_of_people", old_number)

        circuit = instance.circuit
        diff = new_number - old_number

        if diff > 0 and circuit.available_seats < diff:
            return Response({"error": "Not enough seats available"}, status=status.HTTP_400_BAD_REQUEST)

        if diff != 0:
            circuit.available_seats -= diff
            circuit.save()

        total_amount = circuit.price * new_number
        serializer.save(total_amount=total_amount)

        return Response(serializer.data)
