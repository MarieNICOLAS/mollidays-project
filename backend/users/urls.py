from django.urls import path
from .views import UserListView, protected_view

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('protected/', protected_view, name='protected'),
]
