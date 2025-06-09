from django.db import models
from donation.models import Donation, Request

class Receipt(models.Model):
    receipt_id = models.CharField(max_length=10, unique=True)  
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receipt_id:
            last = Receipt.objects.all().order_by('id').last()
            next_id = 1 if not last else last.id + 1
            self.receipt_id = f"RC{next_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt {self.receipt_id}"
