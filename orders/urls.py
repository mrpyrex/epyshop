from django.urls import path
# from .views import CheckoutView
from . import views

app_name = 'orders'

urlpatterns = [
    # path('create/', CheckoutView.as_view(), name='order_create'),
    path('create/', views.order_create, name='order_create'),
    # path('thanks/', views.thanks, name='thanks')
]
