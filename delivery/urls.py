from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    # path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('available-deliveries/', views.available_delivery, name='available_delivery'),
    path('delivery/<int:pk>/', views.delivery_detail, name='delivery_detail'),
    path('mark-delivered/<int:pk>/', views.mark_delivered, name='mark_delivered'),
    path('accept-delivery/<int:pk>/', views.accept_delivery, name='accept_delivery'),
    path('track-delivery/<int:pk>/', views.track_delivery, name='track_delivery'),
    path('active-deliveries/', views.active_delivery, name='active_delivery'),
    path('my-deliveries/', views.my_delivery, name='my_delivery'),
]
