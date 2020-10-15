from django.contrib import admin

# Register your models here.
from customer.models import Profile, ShippingAddress

admin.site.register(Profile)
admin.site.register(ShippingAddress)