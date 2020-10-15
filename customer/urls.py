from django.urls import path
from .views import ContactView,CheckoutView,ProfileView

app_name = 'customer'

urlpatterns = [
    path('contact/',ContactView.as_view(),name='contact'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('checkout/',CheckoutView.as_view(),name='checkout')
]
