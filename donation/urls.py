from django.urls import path
from . import views

app_name = 'donation'

urlpatterns = [
    path('donate/', views.donate_food, name='donate_food'),
    path('my-donations/', views.my_donation, name='my_donation'),
    path('donations/', views.view_donation, name='view_donation'),
    path('donations/<int:pk>/', views.donation_detail, name='donation_detail'),
    path('donations/<int:pk>/request/', views.make_request, name='make_request'),
]
