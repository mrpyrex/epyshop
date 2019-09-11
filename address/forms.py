from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
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
