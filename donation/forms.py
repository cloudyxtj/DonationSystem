from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['food_name', 
                  'description', 
                  'category',
                  'quantity', 
                  'expiry_date', 
                  'address', 
                  'image']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

