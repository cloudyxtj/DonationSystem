from django.urls import path
from . import views

app_name = 'donation'

urlpatterns = [
    path('donate/', views.donate_food, name='donate_food'),
    path('my-donations/', views.my_donation, name='my_donation'),
    path('donations/', views.view_donation, name='view_donation'),
    path('donations/<int:pk>/', views.donation_detail, name='donation_detail'),
    path('my-donations/<int:pk>/', views.modify_donation, name='modify_donation'),
    path('donations/request/<int:pk>/', views.make_request, name='make_request'),
    path('track-requests/', views.track_request, name='track_request'),
    path('track-requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('my-requests/', views.my_request, name='my_request'),
    path('pending-request/', views.pending_request, name='pending_request'),  # Keep it singular here
    path('update-request-status/<int:pk>/', views.update_request_status, name='update_request_status'),
    path('mark-completed/<int:pk>/', views.mark_completed, name='mark_completed'),
]