from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from .models import Address
from django.contrib.auth.models import User, Group

# Create your views here.


class AddressCreateView(CreateView):
    model = Address
    fields = [
        'address_type',
        'billing_address1',
        'billing_address2',
        'phone',
        'country',
        'city',
        'state',
        'post_code'
    ]

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('shop:shop_home')
