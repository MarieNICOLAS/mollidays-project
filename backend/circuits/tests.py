from django.test import TestCase
from django.contrib.auth import get_user_model
from circuits.models import Category, Tag, Circuit
from datetime import date

User = get_user_model()

class CircuitModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Aventure")
        self.tag = Tag.objects.create(name="Montagne")
        self.admin = User.objects.create_superuser(email="admin@test.com", password="admin123")

    def test_create_category(self):
        self.assertEqual(self.category.name, "Aventure")
        self.assertTrue(self.category.is_active)

    def test_create_tag(self):
        self.assertEqual(self.tag.name, "Montagne")

    def test_create_circuit(self):
        circuit = Circuit.objects.create(
            title="Expédition Alpes",
            description="Randonnée de 10 jours dans les Alpes",
            destination="France",
            start_date=date(2025, 6, 10),
            end_date=date(2025, 6, 20),
            price=1200.50,
            duration=10,
            available_seats=15,
            status="active",
            category=self.category
        )
        circuit.tags.add(self.tag)
        self.assertEqual(circuit.title, "Expédition Alpes")
        self.assertEqual(circuit.duration, 10)
        self.assertEqual(circuit.category.name, "Aventure")
        self.assertIn(self.tag, circuit.tags.all())
