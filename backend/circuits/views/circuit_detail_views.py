from rest_framework import generics
from circuits.models.circuit import Circuit
from circuits.serializers.circuit_serializer import CircuitSerializer

class CircuitDetailAPIView(generics.RetrieveAPIView):
    queryset = Circuit.objects.filter(status="active")
    serializer_class = CircuitSerializer
    lookup_field = "id"
