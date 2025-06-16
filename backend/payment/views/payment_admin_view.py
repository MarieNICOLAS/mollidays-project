from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Payment
from ..payment_serializer import PaymentSerializer

class AdminPaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]

class PaymentStatusUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

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

class AdminRefundAllView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        payments = Payment.objects.filter(status='failed')
        payments.update(status='refunded')
        return Response({"message": f"{payments.count()} paiements remboursés."})
