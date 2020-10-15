from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import get_template
from django.views.generic.base import View

from .forms import ContactForm, ShippingAddressForm, ProfileForm
from .models import ShippingAddress, Profile
from product.models import Order


class ProfileView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        instance = get_object_or_404(Profile, username=self.request.user.username)
        form = ProfileForm(self.request.FILES or None, instance=instance)
        context = {
            'form': form,
            'profile': instance
        }
        return render(self.request, 'profile.html', context)

    def post(self, *args, **kwargs):
        form = ProfileForm(self.request.POST, self.request.FILES)
        profile = get_object_or_404(Profile, username=self.request.user.username)
        form.image = self.request.FILES.get('image')
        print(self.request.POST.get('image'))
        print('The form data :', form.data)
        print('The form error :', form)
        if form.is_valid():
            print(form.cleaned_data)
            user = self.request.user
            print(user.email)
            if user:
                profile.username = form.cleaned_data.get('username')
                profile.email = form.cleaned_data.get('email')
                profile.image = form.cleaned_data.get('image')
                profile.save()
                user.username = form.cleaned_data.get('username')
                user.email = form.cleaned_data.get('email')
                user.save()
                messages.info(self.request, 'your account has being updated ')
                return redirect('customer:profile')

        messages.warning(self.request, 'There was an error passing the form pls try again later ')
        return redirect('customer:profile')


class ContactView(View):

    def get(self, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(self.request, 'contact.html', context)

    def post(self, *args, **kwargs):
        print(self.request.POST)
        form = ContactForm(self.request.POST)
        if form.is_valid():
            contact_name = form['name'].value()
            contact_email = form['email'].value()
            contact_subject = form['subject'].value()
            contact_description = form['description'].value()
            print('contact_name :', self.request.POST.get('name'))
            print('contact_email :', self.request.POST.get('email'))
            print('contact_subject :', self.request.POST.get('subject'))
            print('contact_description :', self.request.POST.get('description'))
            template = get_template('contact.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'contact_subject': contact_subject,
                'contact_description': contact_description
            }
            content = template.render(context)
            email = EmailMessage(
                "Email form my ecommerce website ",
                content,
                'www.codertjay@com. djfj cvjvjcom ', ['favourtjay@ghmail.com'],
                headers={'Reply-To': contact_email}
            )
            email.send()
            messages.success(self.request,
                             'Your form has being submitted we would be in touch with you as soon ass possible')
            return redirect('/')
        messages.error(self.request, 'Your form has being submitted we would be in touch with you as soon ass possible')
        return redirect('customer:contact')


class CheckoutView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            order_item_qs = Order.objects.get(user=self.request.user, ordered=False)
        except:
            order_item_qs = None
            messages.warning(self.request, 'you dont have an order ')
            return redirect('core:home')
        try:
            instance = ShippingAddress.objects.get(user=self.request.user)
        except:
            instance = None
        print(instance)
        form = ShippingAddressForm(instance=instance)

        context = {
            'form': form,
            'order_item': order_item_qs
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        order_item_qs = Order.objects.get(user=self.request.user, ordered=False)
        shipping_address = ShippingAddress.objects.get_or_create(user=self.request.user)
        form = ShippingAddressForm(self.request.POST)
        print('cleaned_form', form.data)
        if form.is_valid:
            # print(form.cleaned_data)
            shipping_address.phone_number = form.cleaned_data.get('phone_number')
            shipping_address.state_address = form.cleaned_data.get('state_address')
            shipping_address.other_address = form.cleaned_data.get('other_address')
            shipping_address.apartment_address = form.cleaned_data.get('apartment_address')
            shipping_address.zip_code = form.cleaned_data.get('zip_code')
            shipping_address.save()

            order_item_qs.ordered = True
            order_item_qs.save()

            print('form error', form.errors)
            print('form directories', dir(form))

            form_data = form.save(commit=False)
            form_data.user = self.request.user
            print('cleaned_form', self.request.POST)

            messages.error(self.request, ' there was an error pls try again later')
            return redirect('customer:checkout')

        messages.error(self.request, ' there was an error pls try again leter')
        return redirect('core:cart')
