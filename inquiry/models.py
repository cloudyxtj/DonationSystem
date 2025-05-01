from django.db import models

# Create your models here.

class Inquiry(models.Model):
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('other', 'Other'),
    ]

    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inquiry_type} - {self.subject}"

    class Meta:
        verbose_name_plural = "Inquiries"
