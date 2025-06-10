from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializer import UserSerializer

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
