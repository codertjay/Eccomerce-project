from .models import Product
from django import forms
from django.forms.boundfield import BoundField

class ProductForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = Product
        fields = ['name',
                  'category',
                  'price',
                  'discount_price',
                  'digital',
                  'image',
                  'quantity',
                  'slug',
                  'description']



