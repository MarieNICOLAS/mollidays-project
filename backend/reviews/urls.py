from django.urls import path
from .views import (
    ReviewListCreateView,
    ReviewDetailView,
    CircuitReviewListView,
)
urlpatterns = [
     path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<str:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
    path('circuits/<int:circuit_id>/reviews/', CircuitReviewListView.as_view(), name='circuit-reviews'),
]
