from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)


class Address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=100, choices=ADDRESS_TYPES)
    billing_address1 = models.CharField(max_length=200)
    billing_address2 = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=200, default='Nigeria')
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    post_code = models.CharField(max_length=200, blank=True, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer)
