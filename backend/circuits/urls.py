from django.urls import path, include
from rest_framework.routers import DefaultRouter
from circuits.views.circuit_list_views import CircuitListAPIView
from circuits.views.circuit_detail_views import CircuitDetailAPIView
from circuits.views.circuit_manage_views import CircuitViewSet
from circuits.views.circuit_filter import CircuitFilteredAPIView
from circuits.views.category_views import CategoryListAPIView
from circuits.views.tag_views import TagListAPIView

router = DefaultRouter()
router.register(r'manage', CircuitViewSet, basename='circuit-manage')

urlpatterns = [
    path('', CircuitListAPIView.as_view(), name='circuit-list'),                     # homepage circuits
    path('<int:id>/', CircuitDetailAPIView.as_view(), name='circuit-detail'),       # page detail circuit
    path('search/', CircuitFilteredAPIView.as_view(), name='circuit-filter'),       # page recherche avancée
    path('tags/', TagListAPIView.as_view(), name='tag-list'),                       # liste tags
    path('categories/', CategoryListAPIView.as_view(), name='categories-list'),     # liste catégories
    path('', include(router.urls)),                                                 # CRUD admin
]
