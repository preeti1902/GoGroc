from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category
import json

def getProduct(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        if product.discount:
            original_price = product.price + product.discount
        else:
            original_price = product.price
        context = {
            'product': product,
            'original_price': original_price,
        }
        return render(request, 'store/product.html', context=context)
    except Exception as e:
        print(e)
        return HttpResponse(status=500, content=json.dumps({'error': str(e)}), content_type='application/json')

def getProducts(request):
    products = Product.objects.all()
    category = Category.objects.all()
    for product in products:
        product.original_price = product.price + product.discount if product.discount else product.price
    context = {'products': products, 'categories': category}
    return render(request, 'store/products.html', context)