# scripts/seed_users.py

import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mollidays.settings")
django.setup()

def run():
    User = get_user_model()

    # Superuser
    if not User.objects.filter(email="admin@demo.com").exists():
        User.objects.create_superuser(
            email="admin@demo.com",
            password="admin123",
            first_name="Admin",
            last_name="Demo",
            accept_cgu=True,
            role="admin",
            is_active=True,
        )
        print("✅ Superutilisateur créé : admin@demo.com / admin123")
    else:
        print("⏩ Superutilisateur déjà existant")

    # 10 utilisateurs démo
    user_data = [
        {"first_name": "Alice", "last_name": "Durand", "email": "alice@demo.com"},
        {"first_name": "Bruno", "last_name": "Martin", "email": "bruno@demo.com"},
        {"first_name": "Camille", "last_name": "Lemoine", "email": "camille@demo.com"},
        {"first_name": "David", "last_name": "Moreau", "email": "david@demo.com"},
        {"first_name": "Emma", "last_name": "Bernard", "email": "emma@demo.com"},
        {"first_name": "Farid", "last_name": "Benali", "email": "farid@demo.com"},
        {"first_name": "Gaëlle", "last_name": "Roux", "email": "gaelle@demo.com"},
        {"first_name": "Hugo", "last_name": "Dubois", "email": "hugo@demo.com"},
        {"first_name": "Ismaël", "last_name": "Gomez", "email": "ismael@demo.com"},
        {"first_name": "Julia", "last_name": "Noël", "email": "julia@demo.com"},
    ]

    for user in user_data:
        if not User.objects.filter(email=user["email"]).exists():
            User.objects.create_user(
                email=user["email"],
                password="pass1234",
                first_name=user["first_name"],
                last_name=user["last_name"],
                accept_cgu=True,
                role="user",
                is_active=True,
            )
            print(f"✅ Utilisateur créé : {user['email']}")
        else:
            print(f"⏩ Utilisateur déjà existant : {user['email']}")

if __name__ == "__main__":
    run()
