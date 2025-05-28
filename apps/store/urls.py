from .views import *
from django.urls import path

urlpatterns = [
    path('cart/', cartPage, name='cartPage'),
    path('success/', success, name='success'),
    path('cart/update-quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('cart/summary/', get_cart_summary, name='cart_summary'),
    path('add-address/', addAddress, name='addAddress'),
    path('dashboard/', dashboard, name='dashboard'),
    path('orders/', orderPage, name='orderPage'),
    path('orders/<order_number>/', productOrder, name='productOrder'),
    path('<slug>/', getProduct, name="product"),
    path('', getProducts, name="products"),
    path('addToCart/<uuid>/', addToCart, name='addToCart'),
    path('removeFromCart/<uuid>/', removeFromCart, name='removeFromCart'),
    path('addToWishlist/<uuid:uuid>/', addToWishlist, name='addToWishlist'),
    ]