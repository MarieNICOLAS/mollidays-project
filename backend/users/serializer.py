from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'account_status', 'role']
        extra_kwargs = {
            'account_status': {'read_only': True},
            'role': {'read_only': True}
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    accept_cgu = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password', 'accept_cgu']

    def validate(self, data):
        errors = {}

        if data['password'] != data['confirm_password']:
            errors['password'] = "Les mots de passe ne correspondent pas."

        if not data['accept_cgu']:
            errors['accept_cgu'] = "Les conditions générales doivent être acceptées."

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data.pop('accept_cgu')
        user = User.objects.create_user(**validated_data)
        return user
