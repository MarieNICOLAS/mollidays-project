# scripts/check_seed.py
import os
import django

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mollidays.settings")
django.setup()

from django.contrib.auth import get_user_model
from circuits.models import Circuit, Step, Category, Tag
# from booking.models import Booking
from payment.models import Payment

User = get_user_model()

def run():
    print("🔍 Checking seeded data...")

    assert User.objects.count() >= 11, "❌ Not enough users"
    assert Circuit.objects.count() >= 5, "❌ Not enough circuits"
    assert Step.objects.count() >= 10, "❌ Steps missing"
    assert Category.objects.count() >= 5, "❌ Categories missing"
    assert Tag.objects.count() >= 10, "❌ Tags missing"
    # assert Payment.objects.exists(), "❌ No payments found"

    print("✅ All core demo data present!")

if __name__ == "__main__":
    run()
