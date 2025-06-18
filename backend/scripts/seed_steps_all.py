# scripts/seed_steps_all.py

import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mollidays.settings")
django.setup()

from circuits.models.step import Step
from circuits.models.circuit import Circuit

def run():
    steps_data = {
        "Évasion à Bali": [
            (1, "Arrivée à Denpasar", "Accueil à l’aéroport et transfert à l’hôtel", 2.0),
            (2, "Rizières de Tegallalang", "Balade dans les rizières balinaises", 3.5),
            (3, "Plage de Seminyak", "Temps libre sur la plage", 4.0),
        ],
        "Trésors du Maroc": [
            (1, "Randonnée dans l'Atlas", "Marche dans les montagnes berbères", 4.0),
            (2, "Nuit sous tente", "Soirée dans un bivouac traditionnel", 5.0),
        ],
        "Saveurs d'Italie": [
            (1, "Rome Antique", "Visite du Colisée et du Forum", 2.5),
            (2, "Cours de cuisine à Florence", "Atelier cuisine italienne", 3.0),
        ],
        "Retraite Zen au Japon": [
            (1, "Temple de Kyoto", "Méditation guidée", 1.5),
            (2, "Bambouseraie d’Arashiyama", "Marche en pleine nature", 2.0),
        ],
        "Culture Inca au Pérou": [
            (1, "Cusco", "Exploration de la ville inca", 3.0),
            (2, "Machu Picchu", "Ascension du site légendaire", 5.0),
        ],
    }

    for circuit_title, steps in steps_data.items():
        try:
            circuit = Circuit.objects.get(title=circuit_title)
            for order, title, description, duration_hours in steps:
                step, created = Step.objects.get_or_create(
                    circuit=circuit,
                    order=order,
                    defaults={
                        "title": title,
                        "description": description,
                        "duration_hours": duration_hours,
                        "created_at": datetime.now()
                    }
                )
                print(f"{'✅ Étape ajoutée' if created else '⏩ Étape existe'} : {circuit.title} - {title}")
        except Circuit.DoesNotExist:
            print(f"❌ Circuit non trouvé : {circuit_title}")

if __name__ == "__main__":
    run()
