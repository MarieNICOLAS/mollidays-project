# scripts/seed_categories.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mollidays.settings')
django.setup()

from circuits.models.category import Category

def run():
    categories = [
        ("Plage", "Vacances au soleil et détente au bord de la mer", "🏖️"),
        ("Montagne", "Randonnées, nature et air pur", "🏔️"),
        ("Culture", "Découverte du patrimoine historique", "🏛️"),
        ("Bien-être", "Yoga, méditation, détente", "🧘"),
        ("Gastronomie", "Voyages autour des spécialités locales", "🍽️"),
        ("Aventure", "Expériences uniques et adrénaline", "🚵"),
        ("Nature", "Séjours au cœur de la biodiversité", "🌿"),
        ("Famille", "Moments partagés en toute complicité", "👨‍👩‍👧"),
        ("Histoire", "Explorations de sites anciens", "📜"),
        ("Exotique", "Pays lointains et paysages dépaysants", "🌴"),
    ]

    for name, description, icon in categories:
        cat, created = Category.objects.get_or_create(
            name=name,
            defaults={"description": description, "icon": icon, "is_active": True}
        )
        print(f"{'✅ Créée' if created else '⏩ Existe déjà'} : {cat.name}")

if __name__ == "__main__":
    run()
