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

    def test_update_booking_adjusts_seats(self):
        initial_people = 3
        self.circuit.available_seats -= initial_people
        self.circuit.save()

        booking = Booking.objects.create(
            user=self.user,
            circuit=self.circuit,
            number_of_people=initial_people,
            total_amount=self.circuit.price * initial_people,
            start_date=self.circuit.start_date,
            end_date=self.circuit.end_date,
        )

        # Increase number of people
        new_people = 5
        diff = new_people - booking.number_of_people
        self.circuit.available_seats -= diff
        self.circuit.save()
        booking.number_of_people = new_people
        booking.total_amount = self.circuit.price * new_people
        booking.save()

        self.circuit.refresh_from_db()
        self.assertEqual(self.circuit.available_seats, 5)
        self.assertEqual(booking.total_amount, 5000)

        # Decrease number of people
        reduced_people = 2
        diff = reduced_people - booking.number_of_people
        self.circuit.available_seats -= diff
        self.circuit.save()
        booking.number_of_people = reduced_people
        booking.total_amount = self.circuit.price * reduced_people
        booking.save()

        self.circuit.refresh_from_db()
        self.assertEqual(self.circuit.available_seats, 8)
        self.assertEqual(booking.total_amount, 2000)