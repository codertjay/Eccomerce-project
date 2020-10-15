from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView

# Create your views here.
from .models import Product, OrderItem, Order
from .forms import ProductForm
from django.views.generic.base import View
from django.views.generic import ListView



class Home(ListView):
    model = Product
    template_name = 'homepage.html'
    context_object_name = 'products'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # instance = context['categories']
        context['recent_product'] = Product.objects.all()[0:6]
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        product = Product.objects.all()
        if query:
            object_list = product.filter(
                Q(name__icontains=query) |
                Q(category__icontains=query) |
                Q(description__icontains=query) |
                Q(slug__icontains=query) |
                Q(price__icontains=query) |
                Q(discount_price__icontains=query) |
                Q(time_stamp__icontains=query)
            ).distinct()
        else:
            object_list = Product.objects.all()
        return object_list


def product_category_view(request, category):
    if category:
        print(category)
        queryset = Product.objects.filter(category__icontains=category)
        print(queryset)
        if queryset.exists():
            context = {'products': queryset}
            print(queryset)
            return render(request, 'category.html', context)
        else:
            messages.info(request,'This category does not exist')
            return redirect('core:home')
    else:
        messages.error(request,'There was an error we would get back to you ')
        return redirect('core:home')



@login_required
def cart(request, *args, **kwargs):
    try:
        order_item_qs = Order.objects.get(user=request.user, ordered=False)
        products = Product.objects.all()[:3]
        context = {
            'order_items': order_item_qs,
            'products': products
        }
        return render(request, 'cart.html', context)

    except ObjectDoesNotExist:
        messages.warning(request, 'You do not have an item in your cart ')
        return redirect('/')


class PurchaseItemView(View):
    def get(self,*args,**kwargs):

        return render('purchase.html')


class ProductCreateView(View):

    def get(self, *args, **kwargs):
        form = ProductForm()
        context = {
            'form': form
        }
        return render(self.request, 'create_product.html', context)

    def post(self, *args, **kwargs):
        form = ProductForm(self.request.POST)
        if form.is_valid():
            print('the form is Vaid')
            return redirect('core:detail')


class ProductDetailView(DetailView):
    query_pk_and_slug = 'slug'
    model = Product
    template_name = 'product.html'


@login_required
def add_to_cart(request, slug=None):
    product = get_object_or_404(Product, slug=slug)
    try:
        print('product', product)
        order_item, created = OrderItem.objects.get_or_create(products=product,
                                                              user=request.user,
                                                              ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(products=product).exists():
                # increase the quantity
                order_item.quantity += 1
                order_item.save()
                print('product quantity increased ', order_item.quantity)
                return redirect('core:cart')

            else:
                # add the items to the order
                order.products.add(order_item)
                print('item added ', order_item)
                order.save()
                return redirect('core:cart')

        else:
            # creating an order
            order = Order.objects.create(user=request.user,
                                         ordered=False)
            order.products.add(order_item)
            order_item.save()
            order.save()
            return redirect('core:cart')
    except:
        messages.warning(request, 'An error error occured we are fixing it ')
        return redirect('core:product', slug=product.slug)


@login_required
def remove_single_item_from_cart(request, slug=None):
    product = get_object_or_404(Product, slug=slug)
    try:
        print(product)
        order_item = OrderItem.objects.filter(
            products=product,
            user=request.user,
            ordered=False
        ).first()
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(products=product).exists():
                #  remove single item
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    print('product quantity', order_item.quantity)
                    order_item.save()
                    return redirect('core:cart')

                else:
                    order_item.delete()
                    return redirect('core:cart')
        else:
            print(product)
            return redirect('core:product', slug=product.slug)
    except:
        messages.warning(request, 'An error error occured we are fixing it ')
        return redirect('core:product', slug=product.slug)


@login_required
def remove_items_from_cart(request, slug=None, ):
    product = get_object_or_404(Product, slug=slug)
    try:
        print('product', product)
        order_item = OrderItem.objects.filter(products=product, user=request.user, ordered=False)[0]
        print('order_item', order_item)
        order_qs = Order.objects.filter(user=request.user, ordered=False)[0]
        if order_item:
            if order_qs:
                order_qs.products.remove(order_item)
                OrderItem.delete(order_item)
                print('order_item', order_item)
                return redirect('core:cart')
        else:
            return redirect('core:cart')
    except:
        messages.warning(request, 'An error error occured we are fixing it ')
    return redirect('core:cart')
