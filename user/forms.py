from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_no = forms.CharField(max_length=13, required=True)
    
    ROLE = [
        ('Donor', 'Donor'),
        ('Recipient', 'Recipient'),
        ('Driver', 'Driver'),
    ]
    role = forms.ChoiceField(choices=ROLE)

    class Meta:
        model = User
        fields = ['username', 
                  'email', 
                  'phone_no', 
                  'password1', 
                  'password2', 
                  'role']