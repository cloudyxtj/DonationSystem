from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import uuid

class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
    ]

    deliveryID = models.CharField(max_length=100, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    donationID = models.IntegerField()
    foodName = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending')
    delivery_time = models.DateTimeField(null=True, blank=True)
    proof = models.ImageField(upload_to='delivery_proofs/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.deliveryID:
            self.deliveryID = f"D-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def mark_as_delivered(self, proof_file=None):
        self.status = 'delivered'
        self.delivery_time = timezone.now()
        if proof_file:
            self.proof = proof_file
        self.save()

    def __str__(self):
        return f"Delivery {self.deliveryID} - {self.foodName} - {self.status}"
