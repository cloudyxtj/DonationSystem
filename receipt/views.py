from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from .models import Receipt
from donation.models import Donation, Request

@login_required
def download_receipt(request, pk):
    if request.user.role == 'Donor':
        # Get the completed request for this donation and donor
        request = get_object_or_404(Request, donation__pk=pk, donation__donor=request.user.donor, status='completed')
        receipt, created = Receipt.objects.get_or_create(request=request)
    else:  # Recipient
        request = get_object_or_404(Request, pk=pk, recipient=request.user.recipient, status='completed')
        receipt, created = Receipt.objects.get_or_create(request=request)

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
