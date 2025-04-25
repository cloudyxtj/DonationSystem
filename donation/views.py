from django.shortcuts import render, redirect
from .forms import DonationForm
from .models import Donation
from django.contrib.auth.decorators import login_required
from .strategy import FilterContext, ExpiryDateFilter, QuantityFilter

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
    donations = Donation.objects.filter(status='available')

    filter_type = request.GET.get('filter')
    if filter_type == 'expiry':
        context = FilterContext(ExpiryDateFilter())
    elif filter_type == 'quantity':
        context = FilterContext(QuantityFilter())
    else:
        context = FilterContext(ExpiryDateFilter())  # default

    filter = context.apply_filter(donations)

    return render(request, 'donation/view_donation.html', {
        'donations': filter
    })