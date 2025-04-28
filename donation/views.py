from django.shortcuts import render, redirect, get_object_or_404
from .forms import DonationForm
from .models import Donation
from django.contrib.auth.decorators import login_required
from .strategy import FilterContext, ExpiryDateFilter, QuantityFilter
from django.http import HttpResponseForbidden
from .forms import DonationForm, RequestForm
from .models import Donation, Request

def view_donation(request):
    donations = Donation.objects.filter(status='available')

    # Mapping
    strategies = {
        'expiry': ExpiryDateFilter(),
        'quantity': QuantityFilter(),
        # 'rating': RatingFilter(),  <-- easy to add later
    }

    filter_type = request.GET.get('filter', 'expiry')  # default to 'expiry'
    strategy = strategies.get(filter_type, ExpiryDateFilter())
    
    context = FilterContext(strategy)
    filter = context.apply_filter(donations)

    return render(request, 'donation/view_donation.html', {
        'donations': filter
    })
    
def donation_detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    return render(request, 'donation/donation_detail.html', {'donation': donation})

@login_required
def donate_food(request):
    if not hasattr(request.user, 'donor'):
        return HttpResponseForbidden("You are not authorized to donate food.")
        
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

@login_required
def modify_donation(request, pk):
    # Retrieve the donation instance
    donation = get_object_or_404(Donation, pk=pk)

    # Ensure that the logged-in user is the donor of the donation
    if donation.donor.user != request.user:
        return redirect('donation:view_donation')

    # Ensure the donation is available before allowing modifications
    if donation.status != 'available':
        # Redirect if the donation is not available
        return redirect('donation:view_donation')  # You can redirect to an appropriate page if needed

    if request.method == 'POST':
        if 'save' in request.POST:
            form = DonationForm(request.POST, request.FILES, instance=donation)
            if form.is_valid():
                form.save()
                return redirect('donation:view_donation')
        elif 'delete' in request.POST:
            donation.delete()
            return redirect('donation:view_donation')
    else:
        form = DonationForm(instance=donation)

    return render(request, 'donation/modify_donation.html', {'form': form, 'donation': donation})

@login_required
def make_request(request, pk):
    donation = get_object_or_404(Donation, pk=pk)

    if request.method == 'POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            request_type = form.cleaned_data['request_type']
            address = form.cleaned_data['address']

            # Create a new request entry in the database
            new_request = Request.objects.create(
                donation=donation,
                recipient=request.user.recipient,
                request_type=request_type,
                status='pending',
                address=address if request_type == 'delivery' else None,
            )

            # Update the donation status
            donation.status = 'reserved'
            donation.save()

            return redirect('donation:view_donation')
    else:
        form = RequestForm()

    # Pass the form back to the template, including any errors
    return render(request, 'donation/make_request.html', {
        'donation': donation,
        'form': form,
    })

@login_required
def track_request(request):
    """View for recipients to track their requests."""
    if request.user.role != 'Recipient':
        return redirect('home')
    
    # Get all requests made by the recipient
    requests = Request.objects.filter(
        recipient=request.user.recipient
    ).select_related('donation', 'donation__donor', 'donation__donor__user').order_by('-requested_at')
    
    return render(request, 'donation/track_request.html', {
        'requests': requests
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