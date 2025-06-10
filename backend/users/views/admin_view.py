from rest_framework import generics
from users.serializer import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
