from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Feedback.RATING),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }