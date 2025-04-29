from django.db import models
from user.models import Driver
from donation.models import Donation
from .observers import delivery_status_subject
from django.utils import timezone

class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
    ]

    delivery_id = models.CharField(max_length=10, unique=True, editable=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)  
    food_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending')
    delivery_time = models.DateTimeField(null=True, blank=True)
    proof = models.ImageField(upload_to='delivery_proofs/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.delivery_id:
            last = Delivery.objects.all().order_by('id').last()
            next_id = 1 if not last else last.id + 1
            self.delivery_id = f"DL{next_id:03d}"
        
        # Get the old status before saving
        if self.pk:
            old_status = Delivery.objects.get(pk=self.pk).status
        else:
            old_status = None
        
        # Save the model
        super().save(*args, **kwargs)
        
        # Notify observers if status has changed
        if old_status != self.status:
            delivery_status_subject.notify_observers(
                self.delivery_id,
                old_status,
                self.status
            )

    # def mark_as_delivered(self, proof_file=None):
    #     self.status = 'delivered'
    #     self.delivery_time = timezone.now()
    #     if proof_file:
    #         self.proof = proof_file
    #     self.save()

    def __str__(self):
        return f"Delivery {self.delivery_id}"

class DeliveryLog(models.Model):
    delivery_id = models.CharField(max_length=10)
    old_status = models.CharField(max_length=20, null=True, blank=True)
    new_status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery {self.delivery_id} status changed from {self.old_status} to {self.new_status} at {self.timestamp}"
