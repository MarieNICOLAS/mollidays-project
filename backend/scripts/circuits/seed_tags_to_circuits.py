import os
import sys
from dotenv import load_dotenv

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(BACKEND_DIR)

load_dotenv(os.path.join(BACKEND_DIR, '.env.local'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mollidays.settings')

import django
django.setup()

from circuits.models.circuit import Circuit
from circuits.models.tag import Tag

def run():
    tag_map = {
        "Évasion à Bali": ["Plage", "Relaxation", "Culture"],
        "Montagnes de l'Atlas": ["Aventure", "Randonnée"],
        "Saveurs d'Italie": ["Gastronomie", "Culture"],
        "Retraite Zen au Japon": ["Bien-être", "Culture"],
        "Trésors du Pérou": ["Aventure", "Culture"],
    }

    for circuit_title, tag_names in tag_map.items():
        try:
            circuit = Circuit.objects.get(title=circuit_title)
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                circuit.tags.add(tag)
                print(f"✅ Tag '{tag_name}' ajouté à : {circuit_title}")
        except Circuit.DoesNotExist:
            print(f"❌ Circuit non trouvé : {circuit_title}")

if __name__ == "__main__":
    run()
