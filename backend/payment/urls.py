from django.urls import path
from .views.views import PaymentCreateAPIView, PaymentDetailAPIView, PaymentValidateAPIView
from .views.payment_status_update_view import PaymentStatusUpdateView

urlpatterns = [
    path('payments/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/validate/', PaymentValidateAPIView.as_view(), name='payment-validate'),
    path('payments/<int:pk>/status/', PaymentStatusUpdateView.as_view(), name='payment-status-update'),
]
