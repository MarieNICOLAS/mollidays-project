from django.urls import path
from booking.views import (
    BookingListAPIView,
    BookingCreateAPIView,
    BookingCancelAPIView,
    BookingUpdateAPIView,
    BookingDetailAPIView,
)
from booking.views.booking_status_update_view import BookingStatusUpdateView
from booking.views.my_bookings_view import MyBookingsView


urlpatterns = [
    path('bookings/', BookingListAPIView.as_view(), name='booking-list'),
    path('bookings/book/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/update/', BookingUpdateAPIView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/cancel/', BookingCancelAPIView.as_view(), name='booking-cancel'),
    
    path('bookings/<int:pk>/status/', BookingStatusUpdateView.as_view(), name='booking-status-update'),
    path('me/bookings/', MyBookingsView.as_view(), name='my-bookings'),
]
