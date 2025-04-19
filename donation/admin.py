from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'quantity', 'status', 'expiry_date', 'created_at')
    list_filter = ('status', 'donor')
    search_fields = ('title', 'description', 'donor__username')
