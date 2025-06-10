from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'method', 'status', 'amount', 'transaction_ref', 'date')
    list_filter = ('status', 'method')
    search_fields = ('transaction_ref',)
