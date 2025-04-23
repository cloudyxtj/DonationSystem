from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'quantity', 'expiry_date', 'location')
    list_filter = ('status', 'expiry_date')
    search_fields = ('title', 'location')
