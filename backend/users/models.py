from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    deactivation_date = models.DateTimeField(null=True, blank=True)

    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='active')

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('partner', 'Partner'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']  # important: username est requis par AbstractUser

    def __str__(self):
        return f"{self.email} ({self.role})"
