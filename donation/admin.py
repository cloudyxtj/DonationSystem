from django.contrib import admin
from .models import Donation, Request, Receipt

# @admin.register(Donation)
# class DonationAdmin(admin.ModelAdmin):
#     list_display = ('food_name', 'status', 'quantity', 'expiry_date','category')
#     list_filter = ('status', 'expiry_date')
#     search_fields = ('food_name', 'category')

admin.site.register(Donation)
admin.site.register(Request)
admin.site.register(Receipt)
