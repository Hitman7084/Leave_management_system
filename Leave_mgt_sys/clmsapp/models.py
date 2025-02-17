from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

class User(AbstractUser):
    ROLES = [
        ('Professor', 'Professor'),
        ('Dean', 'Dean'),
        ('Incharge', 'Incharge'),
        ('Student', 'Student'),
    ]
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES, default='Student')

    def __str__(self):
        return self.username

# Create your models here.

class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    # Ignored Now onwards 
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.verified = False
        self.save()
