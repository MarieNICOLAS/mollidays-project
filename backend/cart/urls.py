from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, MyCartView

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = [
    path('carts/my/', MyCartView.as_view(), name='my-cart'),
]
urlpatterns += router.urls