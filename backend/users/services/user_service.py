# backend/users/services/user_service.py
from users.models import User
from django.core.exceptions import ValidationError

class UserService:
    @staticmethod
    def register_user(data):
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError("Un utilisateur avec cet email existe déjà.")
        
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            accept_cgu=data['accept_cgu']
        )
        return user
