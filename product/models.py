from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES = (
    ('cl', 'Cloth'),
    ('ba', 'Bag'),
    ('Fu', 'Furniture'),
    ('Bo', 'Book'),
    ('La', 'Laptop'),
    ('Ph', 'Phone'),
    ('Ca', 'Camera'),
    ('Ch', 'Charger'),
    ('He', 'Headset'),
    ('Mo', 'Mouse'),

)


class Product(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    digital = models.BooleanField(default=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    time_stamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


    @property
    def imageUrl(self):
        try:
            img = self.image.url
        except:
            img = None
        return img

    @property
    def get_price(self):
        if self.discount_price:
            price = self.discount_price
        else:
            price = self.price
        return price


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    time_stamp = models.DateField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.products}--{self.quantity}'

    @property
    def get_product_price(self):
        if self.products.discount_price:
            price = self.products.discount_price * self.quantity
        else:
            price = self.products.price * self.quantity
        return price

    @property
    def get_amount_saved(self):
        if self.products.discount_price:
            if self.products.price:
                saving = self.products.price - self.products.discount_price
        else:
            saving = 0
        return saving


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateField(auto_now_add=True)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.user}--{self.products.count()} products on cart'


    def get_total_price(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_product_price
        print('total: ',total)
        return total
