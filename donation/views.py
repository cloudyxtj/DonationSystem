from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .strategy import FilterContext, ExpiryDateFilter, QuantityFilter
from django.http import HttpResponseForbidden
from .forms import DonationForm, RequestForm
from .models import Donation, Request
from feedback.models import Feedback
from .state import DonationContext
from .decorator import QuantityDecorator, CategoryDecorator
from django.utils import timezone
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from user.decorators import role_required

# Initialize geolocator and rate-limited geocode globally
geolocator = Nominatim(user_agent="share_a_spoon", timeout=5)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=3)

def geocode_address(address):
    try:
        location = geocode(address)
        if location:
            # print returned address for debugging
            print("Geocoded to:", location.address)
            return location.latitude, location.longitude
    except (GeocoderTimedOut, GeocoderUnavailable):
        pass
    return None, None

def view_donation(request):
    today = timezone.now().date()
    Donation.objects.filter(expiry_date__lt=today, status='available').update(status='expired')
    donations = Donation.objects.filter(status='available')

    # Mapping
    strategies = {
        'expiry': ExpiryDateFilter(),
        'quantity': QuantityFilter(),
    }

    filter_type = request.GET.get('filter', 'expiry')  # default to 'expiry'
    strategy = strategies.get(filter_type, ExpiryDateFilter())  

    # Get the minimum quantity from the query parameters (if provided)
    input = request.GET.get('quantity')
    if input:
        try:
            quantity = int(input)
        except ValueError:
            quantity = None  # Invalid quantity input
    else:
        quantity = None

    # Apply the quantity decorator dynamically
    if quantity is not None:
        strategy = QuantityDecorator(strategy, min_quantity=quantity)
    
    # Apply category decorator
    category = request.GET.get('category')
    if category:
        strategy = CategoryDecorator(strategy, category=category)


    context = FilterContext(strategy)  # Applying the decorator
    filter = context.apply_filter(donations)

    # Add pagination (* donations per page)
    paginator = Paginator(filter, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'donation/view_donation.html', {
        'donations': page_obj  # Pass the paginated page object
    })

@login_required    
def donation_detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    # Get all feedbacks related to the donor of this donation
    feedbacks = Feedback.objects.filter(request__donation__donor=donation.donor).select_related('request', 'recipient')

    return render(request, 'donation/donation_detail.html', {
        'donation': donation,
        'feedbacks': feedbacks,
        })

@role_required('Donor')
def donate_food(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user.donor

            # Geocode address
            lat, lon = geocode_address(donation.address)
            if lat is None or lon is None:
                form.add_error('address', "Couldn't locate this address. Please try again.")
                return render(request, 'donation/donate_food.html', {'form': form})
            donation.latitude = lat
            donation.longitude = lon

            donation.save()
            return redirect('donation:my_donation')
    else:
        form = DonationForm()
    return render(request, 'donation/donate_food.html', {'form': form})

@role_required('Donor')
def my_donation(request):
    donations = Donation.objects.filter(donor=request.user.donor).order_by('-created_at')
    return render(request, 'donation/my_donation.html', {'donations': donations})

@role_required('Donor')
def modify_donation(request, pk):
    # Retrieve the donation instance
    donation = get_object_or_404(Donation, pk=pk)
    
    # Ensure that the logged-in user is the donor of the donation
    if donation.donor.user != request.user:
        return redirect('donation:view_donation')

    # Ensure the donation is available before allowing modifications
    if donation.status != 'available':
        # Redirect if the donation is not available
        return redirect('donation:view_donation')

    if request.method == 'POST':
        if 'save' in request.POST:
            form = DonationForm(request.POST, request.FILES, instance=donation)
            if form.is_valid():
                updated_donation = form.save(commit=False)

                # Geocode updated address
                lat, lon = geocode_address(updated_donation.address)
                if lat is None or lon is None:
                    form.add_error('address', "Couldn't locate this address. Please try again.")
                    return render(request, 'donation/modify_donation.html', {
                        'form': form, 
                        'donation': donation,
                    })

                updated_donation.latitude = lat
                updated_donation.longitude = lon
                updated_donation.save()
                return redirect('donation:view_donation')

        elif 'delete' in request.POST:
            donation.delete()
            return redirect('donation:view_donation')
    else:
        form = DonationForm(instance=donation)

    return render(request, 'donation/modify_donation.html', {
        'form': form, 
        'donation': donation,
    })

@role_required('Donor')
def pending_request(request):
    # Get all pending requests (for example, requests that are in 'pending' status)
    pending_requests = Request.objects.filter(status='pending', donation__donor__user=request.user) # Follow the relation: Request -> Donation -> Donor -> User
    return render(request, 'donation/pending_request.html', {'pending_requests': pending_requests})

@role_required('Donor')
def update_request_status(request, pk):
    # Retrieve the specific request by primary key (pk)
    req = get_object_or_404(Request, pk=pk)
    
    # Handle form submission and status change
    if request.method == 'POST':
        new_status = request.POST.get('status')  # Get the status from the form

        if new_status == 'denied':
           # Get the denial reason from the form
            deny_reason = request.POST.get('deny_reason', '').strip()
            req.status = 'denied'
            req.deny_reason = deny_reason  # Save the reason
            req.save()

            # Update the related donation's status to 'available'
            don = req.donation
            don.status = 'available'  # Change donation status to 'available'
            don.save()
        
        elif new_status == 'approved':
            req.status = 'approved'
            req.save()

        return redirect('donation:pending_request')  # Redirect to the pending requests page

    # If not a POST request, render the page (or redirect based on your logic)
    return redirect('donation:pending_request')

@role_required('Recipient')
def make_request(request, pk):
    donation = get_object_or_404(Donation, pk=pk)

    if request.method == 'POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            request_type = form.cleaned_data['request_type']
            address = form.cleaned_data['address']

            # Only geocode if it is delivery
            lat, lon = (None, None)
            if request_type == 'delivery':
                lat, lon = geocode_address(address)
                if lat is None or lon is None:
                    form.add_error('address', "Couldn't locate this address. Please try again.")
                    return render(request, 'donation/make_request.html', {
                        'donation': donation,
                        'form': form,
                    })

            # Create a new request entry in the database
            new_request = Request.objects.create(
                donation=donation,
                recipient=request.user.recipient,
                request_type=request_type,
                status='pending',
                address=address if request_type == 'delivery' else None,
            )

            # Save geolocation if available
            new_request.latitude = lat
            new_request.longitude = lon
            new_request.save()

            # Update the donation status
            context = DonationContext(donation)
            context.reserve()

            return redirect('donation:view_donation')
    else:
        form = RequestForm()

    # Pass the form back to the template, including any errors
    return render(request, 'donation/make_request.html', {
        'donation': donation,
        'form': form,
    })

@role_required('Recipient')
def track_request(request):
    # Get all requests made by the recipient
    requests = Request.objects.filter(
        recipient=request.user.recipient
    ).select_related('donation', 'donation__donor', 'donation__donor__user').order_by('-requested_at')
    return render(request, 'donation/track_request.html', {
        'requests': requests
    })

@role_required('Recipient')
def request_detail(request, pk):    
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

@role_required('Recipient')
def my_request(request):    
    # Get all requests made by the recipient
    requests = Request.objects.filter(
        recipient=request.user.recipient
    ).select_related('donation').order_by('-requested_at')
    
    return render(request, 'donation/my_request.html', {
        'requests': requests
    })

@role_required('Recipient')
def mark_completed(request, pk):
    req = get_object_or_404(Request, pk=pk)
    
    if request.method == 'POST':
        req.status = 'completed'  # Mark the request as completed
        req.save()
    
        # Also update the related donation status to 'collected'
        don = req.donation
        context = DonationContext(don)
        context.collect()

        return redirect('donation:request_detail', pk=req.pk)  # Redirect to the request detail page
    
    return redirect('donation:track_request')
