from django.db import models
from address.models import Address
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.user.first_name} Profile')
