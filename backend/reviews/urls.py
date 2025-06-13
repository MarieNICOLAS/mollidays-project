from django.urls import path
from reviews.review_views import AddReviewView, CircuitReviewListView

urlpatterns = [
    path("reviews/", AddReviewView.as_view(), name="add-review"),
    path("circuits/<int:circuit_id>/reviews/", CircuitReviewListView.as_view(), name="circuit-reviews"),
]
