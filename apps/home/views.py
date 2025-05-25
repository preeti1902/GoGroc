from django.shortcuts import render
from apps.store.models import Product

def  index(request):
    products = Product.objects.all()
    for product in products:
        product.original_price = product.price + product.discount if product.discount else product.price
    context = {
        'products': products
    }
    return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'about/about.html')