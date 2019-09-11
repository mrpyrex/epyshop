from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order, OrderItem
from django.contrib.auth.models import User
from shop.models import Product
from payment.models import Payment


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    paystack_total = int(order.get_total_cost() * 100)
    data_key = settings.PAYSTACK_PUBLIC_KEY
    data_email = request.user.email

    if request.method == 'POST':

        try:
            payment = Payment()
            payment.paystack_id = request.POST['paystack-trxref']
            payment.customer = request.user
            payment.amount = order.get_total_cost()
            payment.save()

            order.paid = True
            order.ref = request.POST['paystack-trxref']
            order.amount = payment
            order.save()

        except ObjectDoesNotExist:
            pass
        return redirect('payment:success')

    context = {
        'order': order,
        'paystack_total': paystack_total,
        'data_key': data_key,
        'data_email': data_email,
    }
    return render(request, 'payment/process.html', context)


def payment_success(request):
    return render(request, 'payment/success.html')


# import hmac
# import hashlib
# import json
# from django.http import HttpResponse

# def processPaystackWebhook(request):
#     """
#     The function takes an http request object
#     containing the json data from paystack webhook client.
#     Django's http request and response object was used
#     for this example.
#     """
#     paystack_sk = "sk_fromthepaystackguys"
#     json_body = json.loads(request.body)
#     computed_hmac = hmac.new(
#         bytes(paystack_sk, 'utf-8'),
#     str.encode(request.body.decode('utf-8')),
#         digestmod=hashlib.sha512
#         ).hexdigest()
#     if 'HTTP_X_PAYSTACK_SIGNATURE' in request.META:
#         if request.META['HTTP_X_PAYSTACK_SIGNATURE'] == computed_hmac:
#             #IMPORTANT! Handle webhook request asynchronously!!
#             #
#             #..code
#             #
#             return HttpResponse(status=200)
#     return HttpResponse(status=400) #non 200
