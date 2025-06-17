from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from unittest.mock import patch

User = get_user_model()

class ReviewAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="test123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch("reviews.views.create_review")
    def test_create_review(self, mock_create):
        mock_create.return_value = {
            "id": "1",
            "user": self.user.id,
            "circuit": 1,
            "rating": 5,
            "comment": "Great",
            "created_at": "2024-01-01T00:00:00",
        }
        response = self.client.post(
            "/api/reviews/",
            {"circuit": 1, "rating": 5, "comment": "Great"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        mock_create.assert_called_once()

    @patch("reviews.views.get_review")
    def test_get_review_detail(self, mock_get):
        mock_get.return_value = {
            "id": "1",
            "user": self.user.id,
            "circuit": 1,
            "rating": 5,
            "comment": "Great",
            "created_at": "2024-01-01T00:00:00",
        }
        response = self.client.get("/api/reviews/1/")
        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once_with("1")

    @patch("reviews.views.get_reviews_for_circuit")
    def test_list_circuit_reviews(self, mock_get):
        mock_get.return_value = []
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/circuits/1/reviews/")
        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once_with(1)

    @patch("reviews.views.get_reviews_for_circuit")
    def test_get_reviews_for_circuit(self, mock_get):
        mock_get.return_value = [
            {
                "id": "507f1f77bcf86cd799439011",
                "user": self.user.id,
                "circuit": 3,
                "rating": 5,
                "comment": "Génial !",
                "created_at": "2025-06-17T12:00:00"
            }
        ]
        response = self.client.get("/api/circuits/3/reviews/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        mock_get.assert_called_once_with(3)
