# scripts/seed_all.py
import sys
import os
import django

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mollidays.settings')
django.setup()

from scripts import (
    seed_users,
    seed_categories,
    seed_tags,
    seed_circuits,
    seed_steps_all,
    seed_payments,
    seed_reviews
)

if __name__ == "__main__":
    print("📦 Début du seed des données de démonstration...")

    seed_users.run()
    seed_categories.run()
    seed_tags.run()
    seed_circuits.run()
    seed_steps_all.run()
    seed_payments.run()
    seed_reviews.run()

    print("✅ Seed complet terminé.")
