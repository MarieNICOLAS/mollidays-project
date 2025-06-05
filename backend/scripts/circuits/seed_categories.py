import os
import sys
from dotenv import load_dotenv

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(BACKEND_DIR)

load_dotenv(os.path.join(BACKEND_DIR, '.env.local'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mollidays.settings')

import django
django.setup()

from circuits.models.category import Category

def run():
    categories_data = [
        {
            "name": "Plage",
            "description": "Vacances au soleil et détente au bord de la mer",
            "icon": "🏖️"
        },
        {
            "name": "Montagne",
            "description": "Aventures et randonnées dans les sommets",
            "icon": "🏔️"
        },
        {
            "name": "Culture",
            "description": "Découverte du patrimoine historique et artistique",
            "icon": "🏛️"
        },
        {
            "name": "Bien-être",
            "description": "Séjours détente, yoga et spas",
            "icon": "🧘"
        },
        {
            "name": "Gastronomie",
            "description": "Voyages autour des spécialités locales",
            "icon": "🍽️"
        },
    ]

    for data in categories_data:
        cat, created = Category.objects.get_or_create(
            name=data["name"],
            defaults={
                "description": data["description"],
                "icon": data["icon"],
                "is_active": True,
            }
        )
        print(f"{'✅ Catégorie créée' if created else '⏩ Existe déjà'} : {cat.name}")

if __name__ == "__main__":
    run()
