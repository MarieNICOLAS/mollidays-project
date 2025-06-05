
import os
import sys
from datetime import date
from dotenv import load_dotenv

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(BACKEND_DIR)

load_dotenv(os.path.join(BACKEND_DIR, '.env.local'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mollidays.settings')

import django
django.setup()

from circuits.models.circuit import Circuit
from circuits.models.category import Category

def run():
    data = [
        {
            "title": "Évasion à Bali",
            "description": "Circuit inoubliable entre rizières, plages et temples sacrés.",
            "destination": "Bali",
            "start_date": date(2025, 7, 10),
            "end_date": date(2025, 7, 20),
            "price": 1499.99,
            "duration": 10,
            "available_seats": 15,
            "status": "active",
            "category_name": "Plage"
        },
        {
            "title": "Montagnes de l'Atlas",
            "description": "Randonnées et nuits berbères au cœur du Maroc.",
            "destination": "Maroc",
            "start_date": date(2025, 8, 5),
            "end_date": date(2025, 8, 15),
            "price": 1199.00,
            "duration": 11,
            "available_seats": 12,
            "status": "active",
            "category_name": "Montagne"
        },
        {
            "title": "Saveurs d'Italie",
            "description": "Parcours gastronomique entre Rome, Florence et Naples.",
            "destination": "Italie",
            "start_date": date(2025, 9, 1),
            "end_date": date(2025, 9, 10),
            "price": 1390.00,
            "duration": 9,
            "available_seats": 20,
            "status": "active",
            "category_name": "Gastronomie"
        },
        {
            "title": "Retraite Zen au Japon",
            "description": "Séjour bien-être entre temples, méditation et nature.",
            "destination": "Japon",
            "start_date": date(2025, 10, 15),
            "end_date": date(2025, 10, 25),
            "price": 1890.00,
            "duration": 10,
            "available_seats": 8,
            "status": "active",
            "category_name": "Bien-être"
        },
        {
            "title": "Trésors du Pérou",
            "description": "Découverte de la culture Inca et du Machu Picchu.",
            "destination": "Pérou",
            "start_date": date(2025, 11, 10),
            "end_date": date(2025, 11, 20),
            "price": 1590.00,
            "duration": 10,
            "available_seats": 10,
            "status": "active",
            "category_name": "Culture"
        },
    ]

    for item in data:
        category, _ = Category.objects.get_or_create(name=item["category_name"])
        obj, created = Circuit.objects.get_or_create(
            title=item["title"],
            defaults={
                "description": item["description"],
                "destination": item["destination"],
                "start_date": item["start_date"],
                "end_date": item["end_date"],
                "price": item["price"],
                "duration": item["duration"],
                "available_seats": item["available_seats"],
                "status": item["status"],
                "category": category
            }
        )
        print(f"{'✅ Circuit créé' if created else '⏩ Existe déjà'} : {obj.title}")

if __name__ == "__main__":
    run()
