from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random
from django.utils import timezone

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

# Leave Request Model(Half assed)
class LeaveApplication(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="leave_requests"
    )
    incharge = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="assigned_leaves",
        limit_choices_to={'role': 'Incharge'}  # Only allow Incharges to be assigned
    )
    message = models.TextField()
    attachment = models.FileField(upload_to='leave_attachments/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Status choices
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved by Incharge', 'Approved by Incharge'),
        ('Rejected by Incharge', 'Rejected by Incharge'),
        ('Forwarded to Dean', 'Forwarded to Dean'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')

    # Incharge review fields
    incharge_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)

    # Dean approval field
    forwarded_to_dean = models.BooleanField(default=False)

    def __str__(self):
        return f"Leave Request ({self.status}) - {self.student.username} to {self.incharge.username if self.incharge else 'Fuck off'}"

