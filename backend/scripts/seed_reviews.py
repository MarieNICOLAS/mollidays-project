# scripts/seed_reviews.py

import os
import django
import random
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mollidays.settings")
django.setup()

from circuits.models.circuit import Circuit
from django.contrib.auth import get_user_model
from reviews.mongo_service import create_review

def run():
    User = get_user_model()
    users = list(User.objects.filter(is_superuser=False))
    circuits = list(Circuit.objects.all())
    comments = [
        "Incroyable expérience, je recommande !",
        "Voyage dépaysant et très bien organisé.",
        "Un souvenir inoubliable avec mon parent.",
        "Accueil parfait, activités variées.",
        "Je repartirai sans hésiter !"
    ]

    for circuit in circuits:
        for _ in range(random.randint(1, 3)):
            user = random.choice(users)
            review = create_review(
                user_id=user.email,
                circuit_id=str(circuit.id),
                rating=random.randint(4, 5),
                comment=random.choice(comments)
            )
            print(f"✅ Avis ajouté pour {circuit.title} par {user.email}")

if __name__ == "__main__":
    run()
