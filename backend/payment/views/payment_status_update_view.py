from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from payment.models import Payment

class PaymentStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Paiement introuvable"}, status=404)

        new_status = request.data.get("status")
        if new_status not in dict(Payment.STATUS_CHOICES):
            return Response({"error": "Statut invalide"}, status=400)

        payment.status = new_status
        payment.save()
        return Response({"message": f"Statut mis à jour : {new_status}"})
