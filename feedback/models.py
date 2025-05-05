from django.db import models

class Feedback(models.Model):
    RATING = [
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    feedback_id = models.CharField(max_length=10, unique=True)
    recipient = models.ForeignKey('user.Recipient', on_delete=models.CASCADE)  
    request = models.ForeignKey('donation.Request', on_delete=models.CASCADE)  
    rating = models.PositiveIntegerField( choices=RATING)
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True) 

    def save(self, *args, **kwargs):
        if not self.feedback_id:
            last = Feedback.objects.all().order_by('id').last()
            next_id = 1 if not last else last.id + 1
            self.feedback_id = f"FB{next_id:03d}"
        super().save(*args, **kwargs)  

    def __str__(self):
        return f"Feedback {self.feedback_id}"
