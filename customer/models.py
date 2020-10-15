from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from product.models import Order
# Create your models here.


class ShippingAddress(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.IntegerField(blank=True,null=True)
    state_address = models.CharField(max_length=50, blank=True, null=True)
    other_address = models.CharField(max_length=100, blank=True, null=True)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10,blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    description = models.TextField()



class Profile(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    image = models.ImageField(upload_to='user',default='user/profile.jpg')

def post_save_user_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(username=instance.username,email=instance.email)
    user_profile, created = Profile.objects.get_or_create(username=instance.username)


post_save.connect(post_save_user_profile_create, sender=settings.AUTH_USER_MODEL)
