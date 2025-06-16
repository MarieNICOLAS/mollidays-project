from django.urls import path
from users.views.auth_view import login_view, register_view
from users.views.profile_view import get_current_user, protected_view
from users.views.admin_view import UserListView
from users.views.password_reset import PasswordResetRequestView, PasswordResetConfirmView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/me/', get_current_user, name='user-me'),
    path('protected/', protected_view, name='protected'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]
