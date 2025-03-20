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
class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('Sick', 'Sick Leave'),
        ('Casual', 'Casual Leave'),
        ('Emergency', 'Emergency Leave'),
        ('Annual', 'Annual Leave'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Forwarded', 'Forwarded'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    file_attachment = models.FileField(upload_to='leave_attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, 
        on_delete=models.SET_NULL, related_name='approved_leaves'
    )

    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.status})"
