from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'account_status', 'role']
        extra_kwargs = {
            'account_status':{'read_only': True},
            'role': {'read_only': True}
        }
