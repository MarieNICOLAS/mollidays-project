from django.urls import path
from .views.views import (
    PaymentCreateAPIView,
    PaymentDetailAPIView,
    PaymentValidateAPIView,
)
from .views.payment_admin_view import (
    AdminPaymentListAPIView,
    PaymentStatusUpdateView,
)

urlpatterns = [
    path('payments/', PaymentCreateAPIView.as_view()),
    path('payments/<int:pk>/', PaymentDetailAPIView.as_view()),
    path('payments/<int:pk>/validate/', PaymentValidateAPIView.as_view()),
    path('payments/admin/', AdminPaymentListAPIView.as_view()),
    path('payments/<int:pk>/status/', PaymentStatusUpdateView.as_view()),
]
