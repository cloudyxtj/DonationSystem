from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Delivery
from donation.models import Request
from django.utils import timezone
from user.models import Driver
from donation.state import DonationContext

@login_required
def available_delivery(request):
    # Get all delivery requests that are approved and not yet assigned to a driver
    available_requests = Request.objects.filter(
        status='approved',
        request_type='delivery'
    ).exclude(
        delivery__isnull=False
    ).select_related('donation', 'donation__donor', 'donation__donor__user')
    
    return render(request, 'delivery/available_delivery.html', {
        'available_requests': available_requests
    })

@login_required
def accept_delivery(request, pk):
    delivery_request = get_object_or_404(Request, pk=pk)
    
    # Check if the request is already assigned to a driver
    if Delivery.objects.filter(request=delivery_request).exists():
        messages.error(request, 'This delivery has already been accepted by another driver.')
        return redirect('delivery:available_delivery')
    
    # Get the driver instance
    driver = get_object_or_404(Driver, user=request.user)
    
    # Create a new delivery entry
    delivery = Delivery.objects.create(
        driver=driver,
        request=delivery_request,
        food_name=delivery_request.donation.food_name,
        status='in_transit'
    )
    
    # Update the donation status
    delivery_request.donation.status = 'reserved'
    delivery_request.donation.save()
    
    messages.success(request, f'You have successfully accepted the delivery of {delivery.food_name}.')
    return redirect('delivery:my_delivery')

@login_required
def active_delivery(request):
    driver = get_object_or_404(Driver, user=request.user)
    active_deliveries = Delivery.objects.filter(
        driver=driver,
        status='in_transit'
    ).select_related('request', 'request__donation', 'request__donation__donor', 'request__donation__donor__user')
    
    return render(request, 'delivery/active_delivery.html', {
        'active_deliveries': active_deliveries
    })

@login_required
def track_delivery(request, pk):
    delivery = get_object_or_404(
        Delivery.objects.select_related(
            'request',
            'request__donation',
            'request__donation__donor',
            'request__donation__donor__user',
            'driver',
            'driver__user'
        ).prefetch_related(
            'request__donation__request_set',
            'request__donation__request_set__recipient',
            'request__donation__request_set__recipient__user'
        ),
        pk=pk
    )
    
    # Verify the driver owns this delivery
    if delivery.driver.user != request.user:
        messages.error(request, 'You can only track your own deliveries.')
        return redirect('delivery:my_delivery')
    
    # Calculate progress
    progress = 0
    if delivery.status == 'in_transit':
        progress = 50
    elif delivery.status == 'delivered':
        progress = 100
    
    return render(request, 'delivery/track_delivery.html', {
        'delivery': delivery,
        'delivery_request': delivery.request,
        'progress': progress
    })

@login_required
def delivery_detail(request, pk):
    delivery = get_object_or_404(
        Delivery.objects.select_related(
            'request',
            'request__donation',
            'request__donation__donor',
            'request__donation__donor__user',
            'driver',
            'driver__user'
        ),
        pk=pk
    )
    
    # Verify the driver owns this delivery
    if delivery.driver.user != request.user:
        messages.error(request, 'You can only view your own deliveries.')
        return redirect('delivery:my_delivery')
    
    return render(request, 'delivery/delivery_detail.html', {
        'delivery': delivery
    })

@login_required
def mark_delivered(request, pk):    
    delivery = get_object_or_404(Delivery, pk=pk)
    
    # Verify the driver owns this delivery
    if delivery.driver.user != request.user:
        messages.error(request, 'You can only update your own deliveries.')
        return redirect('delivery:my_delivery')
    
    if request.method == 'POST':
        proof = request.FILES.get('proof')
        if not proof:
            messages.error(request, 'Please upload proof of delivery.')
            return redirect('delivery:delivery_detail', pk=pk)
        
        # Update delivery status
        delivery.status = 'delivered'
        delivery.delivery_time = timezone.now()
        delivery.proof = proof
        delivery.save()
        
        # Update donation status
        donation = delivery.request.donation
        context = DonationContext(donation)
        context.deliver()
        
        # Update the request status
        req = delivery.request
        req.status = 'completed'
        req.save()

        messages.success(request, 'Delivery has been marked as completed.')
        return redirect('delivery:my_delivery')
    
    return redirect('delivery:delivery_detail', pk=pk)

@login_required
def my_delivery(request):    
    driver = get_object_or_404(Driver, user=request.user)
    deliveries = Delivery.objects.filter(
        driver=driver
    ).select_related('request', 'request__donation', 'request__donation__donor', 'request__donation__donor__user')
    
    return render(request, 'delivery/my_delivery.html', {
        'deliveries': deliveries
    })
