import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

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
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    accept_cgu = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password', 'accept_cgu']

    def validate(self, data):
        errors = {}

        if data['password'] != data['confirm_password']:
            errors['confirm_password'] = "Les mots de passe ne correspondent pas."

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{12,}$'
        if not re.match(pattern, data['password']):
            errors['password'] = (
                "Mot de passe trop faible. Il doit contenir au minimum 12 caractères, "
                "dont au moins une majuscule, une minuscule, un chiffre et un caractère spécial."
            )

        if not data['accept_cgu']:
            errors['accept_cgu'] = "Les conditions générales doivent être acceptées."

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        accept_cgu = validated_data.pop('accept_cgu')  
        user = User.objects.create_user(**validated_data)
        user.accept_cgu = accept_cgu
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Aucun utilisateur avec cet e-mail.")
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = f"http://localhost:3000/reset-password/?uid={user.pk}&token={token}"

        send_mail(
            subject="Réinitialisation de votre mot de passe - Mollidays",
            message=f"Voici le lien pour réinitialiser votre mot de passe : {reset_link}",
            from_email="support@mollidays.com",
            recipient_list=[user.email],
        )
        return reset_link


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            user = User.objects.get(pk=data["uid"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable.")

        if not PasswordResetTokenGenerator().check_token(user, data["token"]):
            raise serializers.ValidationError("Lien invalide ou expiré.")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
