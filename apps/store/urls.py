from .views import getProduct, getProducts, addToCart, addToWishlist
from django.urls import path

urlpatterns = [
    path('<slug>/', getProduct, name="product"),
    path('', getProducts, name="products"),
    path('addToCart/<uuid>/', addToCart, name='addToCart'),
    path('addToWishlist/<uuid:uuid>/', addToWishlist, name='addToWishlist'),
    ]