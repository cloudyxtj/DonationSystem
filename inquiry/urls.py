from django.urls import path
from . import views

app_name = 'inquiry'

urlpatterns = [
    path('', views.inquiry_form, name='form'),
    path('success/', views.inquiry_success, name='success'),
] 