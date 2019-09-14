from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import OrderItem, Order
from address.models import Address
from cart.cart import Cart
from shop.models import Product
from django.conf import settings


@login_required
def order_create(request):
    cart = Cart(request)
    customer = request.user
    try:
        address = Address.objects.get(
            customer=request.user, address_type='billing')
        billing_address1 = address.billing_address1
        billing_address2 = address.billing_address2
        phone = address.phone
        country = address.country
        state = address.state
        city = address.city
        post_code = address.post_code

    except ObjectDoesNotExist:
        return redirect('address:create')

    try:
        order = Order.objects.create(billing_address1=billing_address1, customer=customer, billing_address2=billing_address2,
                                     phone=phone, country=country, state=state, city=city, post_code=post_code)
        if cart.coupon:
            order.coupon = cart.coupon
            order.discount = cart.coupon.discount
        order.save()
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
            print(item['product'].id)
            products = Product.objects.get(id=item['product'].id)
            products.stock = int(
                item['product'].stock - item['quantity'])
            products.save()
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))

    except ObjectDoesNotExist:
        pass

    return render(request, 'orders/create.html', {'cart': cart, 'order_item': order_item, 'customer': customer})
