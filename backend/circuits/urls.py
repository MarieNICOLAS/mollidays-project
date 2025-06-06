from django.urls import path, include
from rest_framework.routers import DefaultRouter
from circuits.views.circuit_views import (
    CircuitListAPIView,
    CircuitDetailAPIView,
    CircuitViewSet
)
from circuits.views.category_views import CategoryListAPIView
from circuits.views.tag_views import TagListAPIView

# 💡 Définir le router ici
router = DefaultRouter()
router.register(r'manage', CircuitViewSet, basename='circuit-manage')

urlpatterns = [
    path('', CircuitListAPIView.as_view(), name='circuit-list'),
    path('<int:id>/', CircuitDetailAPIView.as_view(), name='circuit-detail'),
    path('', include(router.urls)), 
    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('categories/', CategoryListAPIView.as_view(), name='categories-list'),
]
