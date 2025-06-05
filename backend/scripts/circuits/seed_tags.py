import os
import sys
from dotenv import load_dotenv

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(BACKEND_DIR)

load_dotenv(os.path.join(BACKEND_DIR, '.env.local'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mollidays.settings')

import django
django.setup()

from circuits.models.tag import Tag

def run():
    tags = [
        "Plage", "Nature", "Aventure", "Culture", "Randonnée",
        "Gastronomie", "Famille", "Bien-être", "Exotique", "Historique"
    ]

    for tag_name in tags:
        obj, created = Tag.objects.get_or_create(name=tag_name)
        print(f"{'✅ Tag créé' if created else '⏩ Déjà existant'} : {obj.name}")

if __name__ == "__main__":
    run()
