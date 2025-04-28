from django import forms
from .models import Donation, Request

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

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request_type', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your delivery address'})
        }

    def clean_address(self):
        request_type = self.cleaned_data.get('request_type')
        address = self.cleaned_data.get('address')
        
        # Validate address when 'delivery' is selected
        if request_type == 'delivery' and not address:
            raise forms.ValidationError('Please provide a delivery address.')
        return address