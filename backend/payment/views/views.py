from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from ..models import Payment
from ..payment_serializer import PaymentSerializer

class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.validated_data.get("booking")
        if booking.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You cannot create a payment for this booking")
        serializer.save()

class PaymentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(booking__user=user)

class PaymentValidateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            payment = Payment.objects.select_related("booking__user").get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if payment.booking.user != request.user and not request.user.is_staff:
            return Response({"error": "Forbidden"}, status=403)

        if payment.status == "validated":
            return Response({"message": "Already validated"}, status=200)

        payment.status = "validated"
        payment.save()

        booking = payment.booking
        booking.status = "confirmed"
        booking.is_validated = True
        booking.save()

        return Response({"message": "Payment validated"})
