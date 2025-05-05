from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from donation.models import Request

@login_required
def submit_feedback(request, pk):
    donation_request = get_object_or_404(Request, pk=pk)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.recipient = request.user.recipient
            feedback.request = donation_request
            feedback.save()
            return redirect('donation:my_request')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/submit_feedback.html', {
        'form': form,
        'request': donation_request
    })