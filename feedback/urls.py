from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('submit/<int:pk>/', views.submit_feedback, name='submit_feedback'),
]