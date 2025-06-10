from rest_framework import generics
from circuits.models.circuit import Circuit
from circuits.serializers.circuit_serializer import CircuitSerializer

class CircuitFilteredAPIView(generics.ListAPIView):
    serializer_class = CircuitSerializer

    def get_queryset(self):
        qs = Circuit.objects.filter(status="active")
        params = self.request.query_params

        if destination := params.get("destination"):
            qs = qs.filter(destination__icontains=destination)

        if category := params.get("category"):
            qs = qs.filter(category__name__icontains=category)

        if min_price := params.get("min_price"):
            qs = qs.filter(price__gte=min_price)

        if max_price := params.get("max_price"):
            qs = qs.filter(price__lte=max_price)

        if min_duration := params.get("min_duration"):
            qs = qs.filter(duration__gte=min_duration)

        if max_duration := params.get("max_duration"):
            qs = qs.filter(duration__lte=max_duration)

        if start_date := params.get("start_date"):
            qs = qs.filter(start_date__gte=start_date)

        if tags := params.getlist("tags"):
            qs = qs.filter(tags__name__in=tags)

        return qs.distinct()
