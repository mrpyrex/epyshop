from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Payment(models.Model):
    paystack_id = models.CharField(max_length=50)
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.customer)
