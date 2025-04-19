from django.shortcuts import render, redirect
from .forms import DonationForm
from .models import Donation
from django.contrib.auth.decorators import login_required

@login_required
def donate_food(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            return redirect('donation:donation_list')
    else:
        form = DonationForm()
    return render(request, 'donation/donate_food.html', {'form': form})

@login_required
def donation_list(request):
    donations = Donation.objects.filter(donor=request.user)
    return render(request, 'donation/donation_list.html', {'donations': donations})
