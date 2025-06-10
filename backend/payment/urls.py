from django.urls import path
from .views import PaymentCreateAPIView, PaymentDetailAPIView, PaymentValidateAPIView

urlpatterns = [
    path('payments/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/validate/', PaymentValidateAPIView.as_view(), name='payment-validate'),
]
