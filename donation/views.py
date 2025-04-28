from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def request_detail(request, pk):
    """View for recipients to see details of a specific request."""
    if request.user.role != 'Recipient':
        return redirect('home')
    
    # Get the selected request
    selected_request = get_object_or_404(
        Request.objects.select_related('donation', 'donation__donor', 'donation__donor__user'),
        pk=pk,
        recipient=request.user.recipient
    )
    
    # Get all requests for the list
    requests = Request.objects.filter(
        recipient=request.user.recipient
    ).select_related('donation', 'donation__donor', 'donation__donor__user').order_by('-requested_at')
    
    return render(request, 'donation/track_request.html', {
        'requests': requests,
        'selected_request': selected_request
    })

@login_required
def my_request(request):
    """View for recipients to see their requests with map integration."""
    if request.user.role != 'Recipient':
        return redirect('home')
    
    # Get all requests made by the recipient
    requests = Request.objects.filter(
        recipient=request.user.recipient
    ).select_related('donation').order_by('-requested_at')
    
    return render(request, 'donation/my_request.html', {
        'requests': requests
    })

@login_required
def mark_completed(request, pk):
    request_to_mark = get_object_or_404(Request, pk=pk)
    
    if request.method == 'POST':
        request_to_mark.status = 'completed'  # Mark the request as completed
        request_to_mark.save()
    
        # Also update the related donation status to 'collected'
        donation_to_update = request_to_mark.donation
        donation_to_update.status = 'collected'  # Change donation status
        donation_to_update.save()

        return redirect('donation:request_detail', pk=request_to_mark.pk)  # Redirect to the request detail page
    
    return redirect('donation:track_request')

@login_required
def pending_request(request):
    # Get all pending requests (for example, requests that are in 'pending' status)
    pending_requests = Request.objects.filter(status='pending', donation__donor__user=request.user) # Follow the relation: Request -> Donation -> Donor -> User
    return render(request, 'donation/pending_request.html', {'pending_requests': pending_requests})

@login_required
def update_request_status(request, pk):
    # Retrieve the specific request by primary key (pk)
    request_to_update = get_object_or_404(Request, pk=pk)
    
    # Handle form submission and status change
    if request.method == 'POST':
        new_status = request.POST.get('status')  # Get the status from the form

        if new_status == 'denied':
            # Mark the request as denied
            request_to_update.status = 'denied'
            request_to_update.save()

            # Update the related donation's status to 'available'
            donation_to_update = request_to_update.donation
            donation_to_update.status = 'available'  # Change donation status to 'available'
            donation_to_update.save()

        elif new_status == 'approved':
            # If the request is approved, just update the request status (no change to donation status)
            request_to_update.status = 'approved'
            request_to_update.save()
        
        return redirect('donation:pending_request')  # Redirect to the pending requests page

    # If not a POST request, render the page (or redirect based on your logic)
    return redirect('donation:pending_request')
