from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import MyLoginView

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    # path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='app:home'), name='logout'),
]
