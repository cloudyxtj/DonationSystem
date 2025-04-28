from django.db import models
from user.models import Driver
from donation.models import Donation

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
        super().save(*args, **kwargs)

    # def mark_as_delivered(self, proof_file=None):
    #     self.status = 'delivered'
    #     self.delivery_time = timezone.now()
    #     if proof_file:
    #         self.proof = proof_file
    #     self.save()

    def __str__(self):
        return f"Delivery {self.delivery_id}"
