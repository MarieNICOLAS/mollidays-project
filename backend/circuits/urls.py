from django.urls import path
from circuits.views.circuit_views import CircuitListAPIView, CircuitDetailAPIView

urlpatterns = [
    path('', CircuitListAPIView.as_view(), name='circuit-list'),
    path('<int:id>', CircuitDetailAPIView.as_view(), name='circuit-detail'),
]