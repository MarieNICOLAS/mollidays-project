from rest_framework import generics, permissions
from .payment_serializer import PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment

class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentValidateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            payment = Payment.objects.select_related('booking__user').get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if payment.booking.user != request.user and not request.user.is_staff:
            return Response({"error": "Forbidden"}, status=403)

        if payment.status == "validated":
            return Response({"message": "Already validated"}, status=200)

        payment.status = "validated"
        payment.save()

        return Response({"message": "Payment validated"})
