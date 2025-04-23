from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings

class Donation(models.Model):
    STATUS = [
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('delivered', 'Delivered'),
    ]

    donor = models.ForeignKey('user.Donor', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    location = models.TextField(default='Not specified') 
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='donation/', blank=True, null=True)  

    # A ManyToMany field to track recipients who have favorited the donation
    favorite = models.ManyToManyField('user.Recipient', related_name='favorite_donations', blank=True)

    # show what the donation looks like in the admin site --> Nasi Lemak (available)
    def __str__(self):
        return f"{self.title}"