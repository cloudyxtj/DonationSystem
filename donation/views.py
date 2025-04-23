from django.shortcuts import render, redirect
from .forms import DonationForm
from .models import Donation
from django.contrib.auth.decorators import login_required

@login_required
def donate_food(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user.donor
            donation.save()
            return redirect('donation:my_donation')
    else:
        form = DonationForm()
    return render(request, 'donation/donate_food.html', {'form': form})

@login_required
def my_donation(request):
    donations = Donation.objects.filter(donor=request.user.donor)
    return render(request, 'donation/my_donation.html', {'donations': donations})


"""
This view will display all available donations.
"""
def view_donation(request):
    donations = Donation.objects.all()

    # Apply filters if provided
    filter_expiry = request.GET.get('expiry_date')
    filter_rating = request.GET.get('rating')
    filter_quantity = request.GET.get('quantity')

    if filter_expiry:
        donations = donations.filter(expiry_date__lte=filter_expiry)

    if filter_rating:
        donations = donations.filter(rating__gte=filter_rating)  # Assuming rating is a field in your model

    if filter_quantity:
        donations = donations.filter(quantity__gte=filter_quantity)

    return render(request, 'donation/view_donation.html', {'donations': donations})