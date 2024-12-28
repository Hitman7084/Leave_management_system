from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('Professor', 'Professor'),
        ('Dean', 'Dean'),
        ('Incharge', 'Incharge'),
        ('Student', 'Student'),
    ]
    full_name = models.CharField(max_length=100)
    photo = models.ImahgeField(upload_to='photos/', null=True, blank=True)
# Create your models here.
