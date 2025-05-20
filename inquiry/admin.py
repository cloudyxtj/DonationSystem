from django.contrib import admin
from .models import Inquiry

# @admin.register(Inquiry)
# class InquiryAdmin(admin.ModelAdmin):
#     list_display = ('inquiry_type', 'subject', 'email', 'created_at')
#     list_filter = ('inquiry_type', 'created_at')
#     search_fields = ('subject', 'email', 'message')
#     readonly_fields = ('created_at',)
#     ordering = ('-created_at',)

admin.site.register(Inquiry)
