from rest_framework import serializers
from booking.models.booking import Booking
from circuits.serializers.circuit_serializer import CircuitSerializer

class BookingSerializer(serializers.ModelSerializer):
    circuit = CircuitSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'circuit', 'number_of_people', 'total_amount',
            'start_date', 'end_date', 'status', 'is_validated',
            'is_archived', 'created_at'
        ]
        read_only_fields = ['circuit', 'status', 'is_validated', 'is_archived', 'created_at']
