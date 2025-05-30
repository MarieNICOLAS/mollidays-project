from django.urls import path
from .views import UserListView, get_current_user, protected_view, register_view, login_view

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/me/', get_current_user, name='user-me'),
    path('protected/', protected_view, name='protected'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login')
]
