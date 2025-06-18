# scripts/seed_payments.py

import os
import django
import random
import string
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mollidays.settings")
django.setup()

from payment.models import Payment
from booking.models import Booking

def generate_transaction_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def run():
    bookings = Booking.objects.all()

    for booking in bookings:
        if not hasattr(booking, 'payment'):
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.circuit.price * booking.number_of_people,
                transaction_ref=generate_transaction_ref(),
                status=random.choice(["paid", "pending"]),
                paid_at=datetime.now()
            )
            print(f"✅ Paiement ajouté : {payment.transaction_ref}")
        else:
            print(f"⏩ Paiement déjà existant pour booking ID {booking.id}")

if __name__ == "__main__":
    run()
