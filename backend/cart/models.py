from django.db import models
from django.conf import settings
from circuits.models import Circuit
from booking.models.booking import Booking

class Cart(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('converted', 'Converted'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    booking = models.OneToOneField(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='converted_cart')

    def __str__(self):
        return f"Cart #{self.id} - {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    selected_options = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ('cart', 'circuit')

    def __str__(self):
        return f"{self.circuit.title} x{self.quantity}"
