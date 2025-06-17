# backend/cart/serializers.py

from rest_framework import serializers
from .models import Cart, CartItem
from circuits.serializers import CircuitSerializer

class CartItemSerializer(serializers.ModelSerializer):
    circuit = CircuitSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'circuit', 'quantity', 'added_at', 'selected_options']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'booking', 'items']
        read_only_fields = ['user', 'created_at', 'updated_at']
