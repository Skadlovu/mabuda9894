from enum import unique
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Donation
from .forms import DonationForm
import hashlib
import payfast.signals

@csrf_exempt
def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            # Save donation information to the database
            donation = Donation(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                amount=form.cleaned_data['amount'],
                transaction_id='unique_transaction_id',  # Generate a unique ID
                item_name='Donation'
            )
            donation.save()

            # Redirect to PayFast payment page
            # (Note: Replace 'merchant_id' and 'merchant_key' with your PayFast credentials)
            return render(request, 'donations/payment_page.html', {
                'donation': donation,
                'merchant_id': '10032206',
                'merchant_key': '7uh80ghfzbsrz',
                'merchant_passphrase': 'xxxworld.com',
            })
    else:
        form = DonationForm()

    return render(request, 'donations/donation_form.html', {'form': form})


def notify_handler(sender, **kwargs):
    payfast_order=kwargs['order']

    if payfast_order.payment_status=='COMPLETE':
        amount=payfast_order.amount
        transaction_id=payfast_order.transaction_id
    else:
        return'Donation did not go through'
    payfast.signals.notify.connect(notify_handler)



@csrf_exempt
def thankyou(request):
    # Handle PayFast callback
    if request.method == 'POST':
        data = request.POST

        # Verify PayFast payment
        m_payment_id = data.get('m_payment_id')
        payment_status = data.get('payment_status')

        # Perform validation and update the donation status in the database
        if validate_payfast_callback(data):
            donation = Donation.objects.get(transaction_id=m_payment_id)
            donation.status = payment_status
            donation.save()

    return render(request, 'donations/thank_you.html')


def validate_payfast_callback(data):
    # Perform PayFast callback validation here
    # Check the integrity of the data using your PayFast credentials

    # Sample validation (replace with actual validation logic)
    merchant_key = '7uh80ghfzbsrz'
    passphrase = 'xxxworld.com'
    signature = data.get('signature')

    expected_signature = hashlib.md5(f'{merchant_key}|{data.get("m_payment_id")}|{data.get("pf_payment_id")}|{data.get("payment_status")}|{passphrase}'.encode()).hexdigest()

    return signature == expected_signature
