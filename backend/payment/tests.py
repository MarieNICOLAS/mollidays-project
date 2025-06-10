from django.test import TestCase
from booking.models.booking import Booking
from .models import Payment
from django.contrib.auth import get_user_model
from circuits.models import Circuit, Category
from datetime import date

User = get_user_model()

class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="test123")
        self.category = Category.objects.create(name="Test")
        self.circuit = Circuit.objects.create(
            title="Test Circuit",
            description="Test",
            destination="Italie",
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 20),
            price=1000,
            duration=10,
            available_seats=10,
            status="active",
            category=self.category
        )
        self.booking = Booking.objects.create(
            user=self.user,
            circuit=self.circuit,
            number_of_people=2,
            total_amount=2000,
            start_date=self.circuit.start_date,
            end_date=self.circuit.end_date
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=self.booking.total_amount,
            method='cb',
            transaction_ref='TX123456789'
        )
        self.assertEqual(payment.status, 'pending')
        self.assertEqual(payment.amount, 2000)
        self.assertEqual(payment.booking.id, self.booking.id)
