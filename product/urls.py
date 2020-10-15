from django.urls import path

from product.views import (Home,
                           cart,
                           ProductDetailView,
                           add_to_cart,
                           remove_single_item_from_cart ,
                           remove_items_from_cart, ProductCreateView,
                           product_category_view)


app_name = 'core'

urlpatterns = [
    path('', Home.as_view(),name='home'),
    path('cart/', cart,name='cart'),
    path('cart/', cart,name='cart'),
    path('create/', ProductCreateView.as_view(),name='create'),
    path('<str:slug>/', ProductDetailView.as_view(),name='detail'),
    path('product/<str:slug>/add_to_cart/', add_to_cart,name='add_to_cart'),
    path('product/<str:slug>/remove_single_item_from_cart/',remove_single_item_from_cart,name='remove_single_item_from_cart'),
    path('product/<str:slug>/remove_items_from_cart/',remove_items_from_cart,name='remove_items_from_cart'),
    path('product_category/<str:category>/',product_category_view,name='product_category_view'),
]
