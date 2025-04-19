from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    ROLE = [
        ('Donor', 'Donor'),
        ('Recipient', 'Recipient'),
        ('Driver', 'Driver'),
    ]
    role = forms.ChoiceField(choices=ROLE)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
