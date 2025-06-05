from rest_framework import generics
from rest_framework import viewsets, permissions
from circuits.models.circuit import Circuit
from circuits.serializers.circuit_serializer import CircuitSerializer

class CircuitListAPIView(generics.ListAPIView):
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer


class CircuitDetailAPIView(generics.RetrieveAPIView):
    queryset = Circuit.objects.filter(status="active")
    serializer_class = CircuitSerializer
    lookup_field = "id"

class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]