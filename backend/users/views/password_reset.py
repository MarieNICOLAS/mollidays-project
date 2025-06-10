from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializer import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Lien de réinitialisation envoyé par e-mail."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Mot de passe mis à jour avec succès."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
