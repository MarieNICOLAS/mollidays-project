# scripts/seed_tags.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mollidays.settings")
django.setup()

from circuits.models.tag import Tag

def run():
    tags = [
        "Eco-friendly", "Détente", "Slow Travel", "Patrimoine", "Gastronomie",
        "Spiritualité", "Randonnée", "Bien-être", "Famille", "Culture locale",
    ]

    for name in tags:
        tag, created = Tag.objects.get_or_create(name=name)
        print(f"{'✅ Créé' if created else '⏩ Existe déjà'} : {tag.name}")

if __name__ == "__main__":
    run()
