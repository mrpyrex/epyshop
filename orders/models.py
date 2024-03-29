from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from shop.models import Product
from django.contrib.auth.models import User
from payment.models import Payment
from coupons.models import Coupon

# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE, null=True)
    amount = models.ForeignKey(
        Payment, related_name='Payment', on_delete=models.CASCADE, null=True)
    ref = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    billing_address1 = models.CharField(max_length=200, blank=True)
    billing_address2 = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    post_code = models.CharField(max_length=200, blank=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):

        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
