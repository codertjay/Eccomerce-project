from django import forms
from django.contrib.auth.models import User

from .models import ShippingAddress, Profile


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=True,widget=forms.FileInput(attrs={
        'class':'btn btn-info btn-rounded btn-sm waves-effect waves-light'
    }))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control shadow ',
        'label': 'Username'
    }))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={
        'class': 'form-control shadow ',
        'label': 'Email'
    }))

    class Meta:
        model = Profile
        fields = ['username',
                  'email',
                  'image'
                  ]



class ContactForm(forms.Form):
    name = forms.CharField(validators=[], max_length=50, widget=forms.TextInput(attrs={
        'placeholder': ' Your Name ',
        'class': ' form-control shadow ',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email ',
        'class': 'form-control shadow ',

    }))
    subject = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Subject ',
        'class': 'form-control shadow ',
    }))
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={
        'placeholder': ' Content ',
        'class': 'md-textarea form-control shadow ',
        'rows': '5',
        'cols': '20'
    }))

    def clean_email(self):
        email_passed = self.cleaned_data.get('email')
        email_req = 'mmm'
        if email_passed != email_req:
            return forms.ValidationError("Not a valig email pls try again")
        return email_passed


class ShippingAddressForm(forms.ModelForm):
    other_address = forms.CharField(required=False)

    class Meta:
        model = ShippingAddress
        fields = ['phone_number',
                  'state_address',
                  'apartment_address',
                  'other_address',
                  'zip_code']
