from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import UserSerializer
from users.serializer import UserRegisterSerializer
from users.services.user_service import UserService

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    user = request.user
    return Response({
        "message": f"Salut {user.first_name}, tu es bien authentifié !",
        "user": {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    })

@api_view(['POST'])
def register_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Utilisateur créé avec succès !"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None and user.is_active:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    else:
        return Response({'detail': 'Identifiants invalides.'}, status=status.HTTP_401_UNAUTHORIZED)