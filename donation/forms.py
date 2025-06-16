from django import forms
from .models import Donation, Request
from datetime import date

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
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today().isoformat()
        self.fields['expiry_date'].widget.attrs['min'] = today

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request_type', 'address']

    def clean_address(self):
        request_type = self.cleaned_data.get('request_type')
        address = self.cleaned_data.get('address')
        
        # Validate address when 'delivery' is selected
        if request_type == 'delivery' and not address:
            raise forms.ValidationError('Please provide a delivery address.')
        return address