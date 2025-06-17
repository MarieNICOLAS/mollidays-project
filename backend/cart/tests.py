# backend/cart/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from circuits.models import Circuit, Category
from .models import Cart, CartItem

User = get_user_model()

class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="TestCat")
        self.circuit = Circuit.objects.create(
            title="Circuit Test", description="Test", destination="Paris",
            start_date="2025-10-01", end_date="2025-10-10",
            price=1000, duration=10, available_seats=10,
            status="active", category=self.category
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_add_item_to_cart(self):
        response = self.client.post(f"/api/carts/{self.cart.id}/add-item/", {
            "circuit_id": self.circuit.id,
            "quantity": 2
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_remove_item_from_cart(self):
        CartItem.objects.create(cart=self.cart, circuit=self.circuit, quantity=1)
        response = self.client.post(f"/api/carts/{self.cart.id}/remove-item/", {
            "circuit_id": self.circuit.id
        })
        self.assertEqual(response.status_code, 204)
        self.assertEqual(CartItem.objects.count(), 0)
