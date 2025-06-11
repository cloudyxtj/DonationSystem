from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import InquiryForm

def inquiry_form(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            
            # Send email notification
            subject = f'New Inquiry: {inquiry.subject}'
            message = f'''
            Type: {inquiry.get_inquiry_type_display()}
            From: {inquiry.email}
            Subject: {inquiry.subject}
            Message: {inquiry.message}
            '''
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Safe, authenticated sender (email comes from own domain)
                [settings.ADMIN_EMAIL],       # Send to admin
                reply_to=[inquiry.email],     # So admin replies to user
            )
            email.send(fail_silently=False)
            
            # messages.success(request, 'Your inquiry has been sent successfully!')
            return redirect('inquiry:success')
    else:
        form = InquiryForm()
    
    return render(request, 'inquiry/inquiry_form.html', {'form': form})

def inquiry_success(request):
    return render(request, 'inquiry/success.html')
