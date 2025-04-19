from django.urls import path
from . import views

app_name = 'donation'

urlpatterns = [
    path('donate/', views.donate_food, name='donate_food'),
    path('donation-list/', views.donation_list, name='donation_list'),
]
