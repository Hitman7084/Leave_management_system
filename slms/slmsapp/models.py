from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER ={
        (1,'admin'),
        (2,'staff')
    }
    user_type = models.CharField(choices=USER,max_length=50,default=1)

    profile_pic = models.ImageField(upload_to='media/profile_pic')


class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.admin.username


class Staff_Leave(models.Model):

    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=100)
    from_date = models.CharField(max_length=100)
    to_date = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.staff_id.admin.first_name + self.staff_id.admin.last_name 
