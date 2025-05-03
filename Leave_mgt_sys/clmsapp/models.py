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

# dashboard model
class LeaveBalance(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    casual = models.IntegerField(default=10)
    duty = models.IntegerField(default=5)
    medical = models.IntegerField(default=7)
    emergency = models.IntegerField(default=3)

    def deduct(self, leave_type, days):
        if hasattr(self, leave_type):
            setattr(self, leave_type, getattr(self, leave_type) - days)
            self.save()


# Leave Request Model(Half assed)
class LeaveApplication(models.Model):
    LEAVE_CHOICES = [
        ("casual", "Casual Leave"),
        ("duty", "Duty Leave"),
        ("medical", "Medical Leave"),
        ("emergency", "Emergency Leave"),
    ]

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
        limit_choices_to={'role': 'Incharge'}  
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_CHOICES, default="casual")
    message = models.TextField()
    attachment = models.FileField(upload_to='leave_attachments/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True, null=True)
    approval_note = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved by Incharge', 'Approved by Incharge'),
        ('Rejected by Incharge', 'Rejected by Incharge'),
        ('Forwarded to Dean', 'Forwarded to Dean'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Leave Request ({self.status}) - {self.student.username} to {self.incharge.username if self.incharge else 'Fuck off'}"


