from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from booking.models.booking import Booking

class BookingStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]  

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({"detail": "Réservation non trouvée."}, status=404)

        new_status = request.data.get("status")
        if new_status not in dict(Booking.STATUS_CHOICES):
            return Response({"detail": "Statut invalide."}, status=400)

        booking.status = new_status
        booking.save()
        return Response({"message": f"Statut mis à jour : {new_status}"}, status=200)
