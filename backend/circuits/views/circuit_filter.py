from rest_framework import generics
from circuits.models.circuit import Circuit
from circuits.serializers.circuit_serializer import CircuitSerializer
from datetime import date

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
            try:
                qs = qs.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price := params.get("max_price"):
            try:
                qs = qs.filter(price__lte=float(max_price))
            except ValueError:
                pass

        if min_duration := params.get("min_duration"):
            try:
                qs = qs.filter(duration__gte=int(min_duration))
            except ValueError:
                pass

        if max_duration := params.get("max_duration"):
            try:
                qs = qs.filter(duration__lte=int(max_duration))
            except ValueError:
                pass

        if start_date := params.get("start_date"):
            try:
                qs = qs.filter(start_date__gte=date.fromisoformat(start_date))
            except ValueError:
                pass

        if tags := params.getlist("tags"):
            qs = qs.filter(tags__name__in=tags)

        return qs.distinct()
