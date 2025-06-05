from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from .models import Receipt
from donation.models import Donation, Request

@login_required
def download_receipt(request, pk):
    # Get the donation or request based on the user's role
    if request.user.role == 'Donor':
        donation = get_object_or_404(Donation, pk=pk, donor=request.user.donor)
        # Get or create receipt for donor
        receipt, created = Receipt.objects.get_or_create(
            donation=donation,
            defaults={
                'request': Request.objects.get(donation=donation, status='completed'),
                'donor': donation.donor,
                'recipient': Request.objects.get(donation=donation, status='completed').recipient
            }
        )
    else:  # Recipient
        donation_request = get_object_or_404(Request, pk=pk, recipient=request.user.recipient)
        # Get or create receipt for recipient
        receipt, created = Receipt.objects.get_or_create(
            request=donation_request,
            defaults={
                'donation': donation_request.donation,
                'donor': donation_request.donation.donor,
                'recipient': request.user.recipient
            }
        )

    # Render the template
    template = get_template('receipt/download_receipt.html')
    html = template.render({'receipt': receipt})

    # Create the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="receipt_{receipt.receipt_id}.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(
        html, dest=response,
        encoding='utf-8'
    )

    if pisa_status.err:
        return HttpResponse('Error generating the PDF. Please try again later.')

    return response
