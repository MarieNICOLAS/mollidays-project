# scripts/seed_tags_to_circuits.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mollidays.settings")
django.setup()

from circuits.models.circuit import Circuit
from circuits.models.tag import Tag

def run():
    mapping = {
        "Évasion à Bali": ["Plage", "Bien-être", "Eco-friendly"],
        "Trésors du Maroc": ["Aventure", "Randonnée", "Famille"],
        "Saveurs d'Italie": ["Gastronomie", "Culture locale"],
        "Retraite Zen au Japon": ["Spiritualité", "Slow Travel"],
        "Culture Inca au Pérou": ["Histoire", "Nature"],
    }

    for circuit_title, tag_names in mapping.items():
        try:
            circuit = Circuit.objects.get(title=circuit_title)
            tags = Tag.objects.filter(name__in=tag_names)
            circuit.tags.set(tags)
            circuit.save()
            print(f"✅ Tags ajoutés à : {circuit_title}")
        except Circuit.DoesNotExist:
            print(f"❌ Circuit non trouvé : {circuit_title}")

if __name__ == "__main__":
    run()
