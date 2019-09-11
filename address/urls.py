from django.urls import path
from .views import AddressCreateView


app_name = 'address'

urlpatterns = [
    path('create/', AddressCreateView.as_view(), name='create')
]
