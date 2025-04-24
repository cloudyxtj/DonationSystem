from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('deliveryID', 'foodName', 'status', 'user', 'delivery_time')
    list_filter = ('status',)
    search_fields = ('deliveryID', 'foodName', 'user__username')