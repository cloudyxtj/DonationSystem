from django.shortcuts import render
from donation.models import Donation

def home_view(request):
    # Count total donations
    total_donations = Donation.objects.count()
    
    # Count successful donations (those that have been delivered)
    successful_donations = Donation.objects.filter(status='delivered').count()
    
    context = {
        'total_meals': total_donations,
        'completed_deals': successful_donations,
    }
    return render(request, 'app/home.html', context)