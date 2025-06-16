from django.urls import path, include
from rest_framework.routers import DefaultRouter
from booking.views import (
    BookingListAPIView,
    BookingCreateAPIView,
    BookingCancelAPIView,
    BookingUpdateAPIView,
    BookingDetailAPIView,
)
from booking.views.booking_status_update_view import BookingStatusUpdateView
from booking.views.my_bookings_view import MyBookingsView
from booking.views.admin_booking_view import AdminBookingViewSet

router = DefaultRouter()
router.register(r'bookings/manage', AdminBookingViewSet, basename='booking-manage')

urlpatterns = [
    path('bookings/', BookingListAPIView.as_view(), name='booking-list'),
    path('bookings/book/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/update/', BookingUpdateAPIView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/cancel/', BookingCancelAPIView.as_view(), name='booking-cancel'),
    
    path('bookings/<int:pk>/status/', BookingStatusUpdateView.as_view(), name='booking-status-update'),
    path('me/bookings/', MyBookingsView.as_view(), name='my-bookings'),
]

urlpatterns += router.urls