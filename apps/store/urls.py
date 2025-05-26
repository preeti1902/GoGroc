from .views import getProduct, getProducts, addToCart, addToWishlist, cartPage, dashboard
from django.urls import path

urlpatterns = [
    path('cart/', cartPage, name='cartPage'),
    path('dashboard/', dashboard, name='dashboard'),
    path('<slug>/', getProduct, name="product"),
    path('', getProducts, name="products"),
    path('addToCart/<uuid>/', addToCart, name='addToCart'),
    path('addToWishlist/<uuid:uuid>/', addToWishlist, name='addToWishlist'),
    ]