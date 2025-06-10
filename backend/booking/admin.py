from django.contrib import admin
from booking.models.booking import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'circuit', 'number_of_people', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'is_validated')
    search_fields = ('user__email', 'circuit__title')
