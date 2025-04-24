from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('driver_dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('delivery_detail/<str:delivery_id>/', views.delivery_detail, name='delivery_detail'),
    path('mark_delivered/', views.mark_delivered, name='mark_delivered'),
]
