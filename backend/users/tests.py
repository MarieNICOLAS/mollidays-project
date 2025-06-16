from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTokenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="secure1234",
            first_name="Test",
            last_name="User",
            accept_cgu=True
        )

    def test_login_and_token_refresh(self):
        # Login first
        response = self.client.post(reverse("login"), {
            "email": "testuser@example.com",
            "password": "secure1234"
        })
        self.assertEqual(response.status_code, 200)
        access = response.data["access"]
        refresh = response.data["refresh"]

        # Refresh token
        response_refresh = self.client.post(reverse("token-refresh"), {
            "refresh": refresh
        })
        self.assertEqual(response_refresh.status_code, 200)
        self.assertIn("access", response_refresh.data)

    def test_logout_blacklists_token(self):
        response = self.client.post(reverse("login"), {
            "email": "testuser@example.com",
            "password": "secure1234"
        })
        refresh = response.data["refresh"]

        response_logout = self.client.post(reverse("logout"), {
            "refresh": refresh
        })
        self.assertIn(response_logout.status_code, [200, 205])


    def test_invalid_refresh_token(self):
        response = self.client.post(reverse("token-refresh"), {
            "refresh": "invalidtoken"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.data)
