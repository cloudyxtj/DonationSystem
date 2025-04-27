from django.shortcuts import render, redirect, get_object_or_404
from .forms import DonationForm
from .models import Donation, Request
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
    
def donation_detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    return render(request, 'donation/donation_detail.html', {'donation': donation})

def request_donation(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)

    if request.method == 'POST' and donation.recipient == request.user:
        # Process the donation request here
        donation.status = 'Requested'  # Example: mark the donation as requested
        donation.save()

        return redirect('donation:view_donation', donation_id=donation.id)

    return redirect('donation:view_donation')

@login_required
def make_request(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    
    if request.method == 'POST':
        # Create a new request
        new_request = Request.objects.create(
            donation=donation,
            recipient=request.user.recipient,
            status='pending'
        )
        
        # Update donation status
        donation.status = 'reserved'
        donation.save()
        
        return redirect('donation:view_donation')
        
    return render(request, 'donation/make_request.html', {'donation': donation})