from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE = (
        ('Admin', 'Admin'),
        ('Donor', 'Donor'),
        ('Recipient', 'Recipient'),
        ('Driver', 'Driver'),
    )
    role = models.CharField(max_length=20, choices=ROLE)
    phone_no = models.CharField(max_length=13, blank=True)

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}"

class Recipient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}"
    
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.user.username}"
