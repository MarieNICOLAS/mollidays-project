import os
import sys
from datetime import datetime
from dotenv import load_dotenv

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(BACKEND_DIR)

load_dotenv(os.path.join(BACKEND_DIR, '.env.local'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mollidays.settings')

import django
django.setup()

from circuits.models.step import Step
from circuits.models.circuit import Circuit

def run():
    steps_data = {
        "Évasion à Bali": [
            ("Arrivée à Denpasar", "Accueil à l’aéroport et transfert à l’hôtel.", 1, 2.0),
            ("Visite des rizières de Tegallalang", "Exploration emblématique des paysages balinais.", 2, 3.5),
            ("Détente à la plage de Seminyak", "Temps libre à la plage.", 3, 4.0),
        ],
        "Montagnes de l'Atlas": [
            ("Randonnée dans la vallée", "Marche dans les paysages berbères.", 1, 3.0),
            ("Nuit sous tente", "Soirée en bivouac traditionnel.", 2, 4.5),
        ],
        "Saveurs d'Italie": [
            ("Rome Antique", "Visite du Colisée et du Forum.", 1, 2.5),
            ("Cuisine Toscane", "Cours de cuisine locale à Florence.", 2, 3.5),
        ],
        "Retraite Zen au Japon": [
            ("Temple de Kyoto", "Méditation guidée dans un temple zen.", 1, 1.5),
            ("Balade en forêt", "Marche dans la bambouseraie d’Arashiyama.", 2, 2.5),
        ],
        "Trésors du Pérou": [
            ("Cusco", "Découverte du patrimoine inca.", 1, 3.0),
            ("Machu Picchu", "Ascension du site mythique.", 2, 5.0),
        ],
    }

    for circuit_title, steps in steps_data.items():
        try:
            circuit = Circuit.objects.get(title=circuit_title)
            for title, desc, order, hours in steps:
                step, created = Step.objects.get_or_create(
                    circuit=circuit,
                    order=order,
                    defaults={
                        "title": title,
                        "description": desc,
                        "duration_hours": hours,
                        "created_at": datetime.now()
                    }
                )
                print(f"{'✅ Créée' if created else '⏩ Déjà existante'} : {circuit_title} – Étape {order}")
        except Circuit.DoesNotExist:
            print(f"❌ Circuit non trouvé : {circuit_title}")

if __name__ == "__main__":
    run()
