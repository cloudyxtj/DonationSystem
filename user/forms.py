from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User
from django.core.exceptions import ValidationError

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

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('instance')  # the user being edited
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if User.objects.exclude(pk=self.user.pk).filter(phone_no=phone_no).exists():
            raise ValidationError("This phone number is already in use.")
        return phone_no

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'