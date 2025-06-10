import os
import sys
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mollidays.settings")

import django
django.setup()

from circuits.models.circuit import Circuit
from circuits.models.category import Category

def run():
    beach_category, _ = Category.objects.get_or_create(
        name="Plage", 
        defaults={"description": "Vacances au soleil"}
    )

    circuit, created = Circuit.objects.get_or_create(
        title="Évasion à Bali",
        defaults={
            "description": "Profitez d’un circuit inoubliable entre rizières, plages et temples sacrés à Bali.",
            "destination": "Bali",
            "start_date": date(2025, 7, 10),
            "end_date": date(2025, 7, 20),
            "price": 1499.99,
            "duration": 10,
            "available_seats": 15,
            "status": "active",
            "category": beach_category,
        }
    )

    if created:
        print("✅ Circuit créé :", circuit)
    else:
        print("⚠️ Circuit déjà existant :", circuit)

if __name__ == "__main__":
    run()