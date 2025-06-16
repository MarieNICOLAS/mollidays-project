from django.test import TestCase
from rest_framework.test import APIClient
from booking.models.booking import Booking
from .models import Payment
from django.contrib.auth import get_user_model
from circuits.models import Circuit, Category
from datetime import date

User = get_user_model()

class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="test123")
        self.other_user = User.objects.create_user(email="other@example.com", password="test123")
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
        self.other_booking = Booking.objects.create(
            user=self.other_user,
            circuit=self.circuit,
            number_of_people=1,
            total_amount=1000,
            start_date=self.circuit.start_date,
            end_date=self.circuit.end_date
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

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

    def test_user_cannot_create_payment_for_other_booking(self):
        response = self.client.post('/api/payments/', {
            'booking': self.other_booking.id,
            'amount': 1000,
            'method': 'cb'
        })
        self.assertIn(response.status_code, [400, 403])

    def test_user_cannot_retrieve_other_payment(self):
        other_payment = Payment.objects.create(
            booking=self.other_booking,
            amount=1000,
            method='cb',
            transaction_ref='TX2'
        )
        response = self.client.get(f'/api/payments/{other_payment.id}/')
        self.assertEqual(response.status_code, 404)
    
    def test_admin_can_refund_payment(self):
        self.admin = User.objects.create_superuser(email="admin@example.com", password="admin123")
        self.client.force_authenticate(user=self.admin)
        payment = Payment.objects.create(
            booking=self.booking,
            amount=2000,
            method='cb',
            transaction_ref='TXADMIN'
        )
        response = self.client.patch(f'/api/payments/{payment.id}/status/', {
            "status": "refunded"
        }, format="json")

        self.assertEqual(response.status_code, 200)
        payment.refresh_from_db()
        self.assertEqual(payment.status, "refunded")

    def test_validate_payment_updates_booking(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=self.booking.total_amount,
            method='cb',
            transaction_ref='TXVALID'
        )
        response = self.client.patch(f'/api/payments/{payment.id}/validate/')
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'validated')
        self.assertEqual(self.booking.status, 'confirmed')
        self.assertTrue(self.booking.is_validated)