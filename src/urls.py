"""django_razorpay URL Configuration
"""
from django.urls import path,include
from .views import coffee_payment,payment_status



urlpatterns = [
    path('', coffee_payment, name='coffee-payment'),
    path('payment-status',payment_status,name='payment-status')

]
