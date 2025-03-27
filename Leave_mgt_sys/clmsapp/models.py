from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
import random

# Custom User Model
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

# OTP Verification Model
class OTPVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.verified = False
        self.created_at = timezone.now()  # Update timestamp when OTP is generated
        self.save()

# Leave Request Model
class LeaveApplication(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(upload_to='leave_files/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leave Request by {self.student.username}"
