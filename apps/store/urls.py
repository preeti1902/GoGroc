from .views import getProduct
from django.urls import path

urlpatterns = [
    path('<slug>/', getProduct, name="product")]