from django.urls import path, include
from rest_framework.routers import DefaultRouter
from circuits.views.circuit_views import (
    CircuitListAPIView,
    CircuitDetailAPIView,
    CircuitViewSet
)

# 💡 Définir le router ici
router = DefaultRouter()
router.register(r'manage', CircuitViewSet, basename='circuit-manage')

urlpatterns = [
    path('', CircuitListAPIView.as_view(), name='circuit-list'),
    path('<int:id>/', CircuitDetailAPIView.as_view(), name='circuit-detail'),
    path('', include(router.urls)),  # Inclure les routes du ViewSet
]
