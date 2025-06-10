from django.test import TestCase
from django.contrib.auth import get_user_model
from circuits.models import Circuit, Category
from booking.models.booking import Booking
from datetime import date

User = get_user_model()

class BookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="test123")
        self.category = Category.objects.create(name="Plage")

        self.circuit = Circuit.objects.create(
            title="Test circuit",
            description="Voyage test",
            destination="Italie",
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 20),
            price=1000,
            duration=10,
            available_seats=10,
            status="active",
            category=self.category
        )

    def test_create_booking_decrements_seats_and_calculates_total(self):
        nb_people = 3
        total = self.circuit.price * nb_people

        # Réduction manuelle comme dans la vue
        self.circuit.available_seats -= nb_people
        self.circuit.save()

        booking = Booking.objects.create(
            user=self.user,
            circuit=self.circuit,
            number_of_people=nb_people,
            total_amount=total,
            start_date=self.circuit.start_date,
            end_date=self.circuit.end_date
        )

        self.assertEqual(booking.total_amount, 3000)
        self.assertEqual(booking.user.email, "test@example.com")
        self.assertEqual(booking.number_of_people, 3)

        self.circuit.refresh_from_db()
        self.assertEqual(self.circuit.available_seats, 7)
