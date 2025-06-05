import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Chemin du dossier backend/
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(BACKEND_DIR)

# Charger les variables d’environnement depuis backend/.env.local
load_dotenv(os.path.join(BACKEND_DIR, '.env.local'))

# Définir le module de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mollidays.settings')

import django
django.setup()

from circuits.models.step import Step
from circuits.models.circuit import Circuit

def run():
    try:
        circuit = Circuit.objects.get(title="Évasion à Bali")
        steps_data = [
            {
                "order": 1,
                "title": "Arrivée à Denpasar",
                "description": "Accueil à l’aéroport et transfert à l’hôtel.",
                "duration_hours": 2.0,
            },
            {
                "order": 2,
                "title": "Visite des rizières de Tegallalang",
                "description": "Exploration des paysages emblématiques.",
                "duration_hours": 3.5,
            },
            {
                "order": 3,
                "title": "Détente à la plage de Seminyak",
                "description": "Moment libre pour profiter du sable chaud.",
                "duration_hours": 4.0,
            },
        ]

        for step in steps_data:
            obj, created = Step.objects.get_or_create(
                circuit=circuit,
                order=step["order"],
                defaults={
                    "title": step["title"],
                    "description": step["description"],
                    "duration_hours": step["duration_hours"],
                    "created_at": datetime.now()
                }
            )
            print(f"{'✅ Étape ajoutée' if created else '⏩ Étape déjà existante'} : {obj.title}")

    except Circuit.DoesNotExist:
        print("❌ Le circuit 'Évasion à Bali' n'existe pas. Crée-le d'abord.")

if __name__ == "__main__":
    run()
