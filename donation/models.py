from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
# from django.conf import settings

class Donation(models.Model):
    STATUS = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('collected', 'Collected'),
        ('delivered', 'Delivered'),
    ]

    CATEGORY = [
        ('cooked', 'Cooked Food'),
        ('packaged', 'Packaged Food'),
        ('canned', 'Canned Goods'),
        ('baked', 'Baked Goods'),
        ('others', 'Others'),
    ]
    
    donation_id = models.CharField(max_length=10, unique=True, blank=True)
    donor = models.ForeignKey('user.Donor', on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY, default='others')
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    address = models.TextField() 
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='donation/', blank=True, null=True)  

    # A ManyToMany field to track recipients who have favorited the donation
    favorite = models.ManyToManyField('user.Recipient', related_name='favorite_donations', blank=True)

    def save(self, *args, **kwargs):
        if not self.donation_id:
            last = Donation.objects.all().order_by('id').last()
            next_id = 1 if not last else last.id + 1
            self.donation_id = f"DN{next_id:03d}"
        super().save(*args, **kwargs)

    # show what the donation looks like in the admin site --> Nasi Lemak
    def __str__(self):
        return f"{self.title}"
    
class Request(models.Model):
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    request_id = models.CharField(max_length=10, unique=True)  
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)  
    recipient = models.ForeignKey('user.Recipient', on_delete=models.CASCADE)  
    requested_at = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='pending')

    def save(self, *args, **kwargs):
        if not self.request_id:
            last = Request.objects.all().order_by('id').last()
            next_id = 1 if not last else last.id + 1
            self.request_id = f"RQ{next_id:03d}"
        super().save(*args, **kwargs)  

    def __str__(self):
        return f"Request {self.request_id}"
    
class Receipt(models.Model):
    receipt_id = models.CharField(max_length=10, unique=True)  
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)  
    request = models.ForeignKey('Request', on_delete=models.CASCADE)
    donor = models.ForeignKey('user.Donor', on_delete=models.CASCADE)
    recipient = models.ForeignKey('user.Recipient', on_delete=models.CASCADE)
    generated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.receipt_id:
            last = Receipt.objects.all().order_by('id').last()
            next_id = 1 if not last else last.id + 1
            self.receipt_id = f"RC{next_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt {self.receipt_id}"