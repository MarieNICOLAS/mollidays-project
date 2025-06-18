# backend/cart/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
from circuits.models import Circuit
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        cart = self.get_object()
        circuit_id = request.data.get('circuit_id')
        quantity = int(request.data.get('quantity', 1))
        options = request.data.get('selected_options', {})

        circuit = get_object_or_404(Circuit, id=circuit_id)

        item, created = CartItem.objects.get_or_create(cart=cart, circuit=circuit)
        if not created:
            item.quantity += quantity
        item.selected_options = options
        item.save()

        return Response(CartItemSerializer(item).data, status=201)

    @action(detail=True, methods=['post'], url_path='remove-item')
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        circuit_id = request.data.get('circuit_id')
        item = get_object_or_404(CartItem, cart=cart, circuit_id=circuit_id)
        item.delete()
        return Response({"message": "Item removed."}, status=204)

class MyCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)