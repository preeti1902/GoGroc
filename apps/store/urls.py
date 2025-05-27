from .views import getProduct, getProducts, addToCart, addToWishlist, cartPage, dashboard, orderPage, productOrder
from django.urls import path

urlpatterns = [
    path('cart/', cartPage, name='cartPage'),
    path('dashboard/', dashboard, name='dashboard'),
    path('orders/', orderPage, name='orderPage'),
    path('orders/orderId/', productOrder, name='productOrder'),
    path('<slug>/', getProduct, name="product"),
    path('', getProducts, name="products"),
    path('addToCart/<uuid>/', addToCart, name='addToCart'),
    path('addToWishlist/<uuid:uuid>/', addToWishlist, name='addToWishlist'),
    ]