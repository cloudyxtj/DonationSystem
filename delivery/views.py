from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Delivery

@login_required
def driver_dashboard(request):
    print("Driver dashboard view called")  # Debug print
    deliveries = Delivery.objects.filter(user=request.user)
    context = {
        'deliveries': deliveries,
        'user': request.user,
    }
    return render(request, 'delivery/driver_dashboard.html', context)

def delivery_detail(request, delivery_id):
    delivery = get_object_or_404(Delivery, deliveryID=delivery_id)
    return render(request, 'delivery/delivery_detail.html', {'delivery': delivery})

@login_required
def mark_delivered(request, delivery_id):
    delivery = get_object_or_404(Delivery, deliveryID=delivery_id)
    if request.method == 'POST':
        proof = request.FILES.get('proof')
        delivery.mark_as_delivered(proof)
        return redirect('delivery/delivery_detail', delivery_id=delivery.deliveryID)
    return render(request, 'delivery/mark_delivered.html', {'delivery': delivery})