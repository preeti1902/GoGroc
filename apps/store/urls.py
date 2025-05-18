from .views import getProduct, getProducts
from django.urls import path

urlpatterns = [
    path('<slug>/', getProduct, name="product"),
    path('', getProducts, name="products")
    ]