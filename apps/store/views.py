from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
import json

def getProduct(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        context = {'product': product}
        return render(request, 'store/product.html', context=context)
    except Exception as e:
        print(e)
        return HttpResponse(status=500, content=json.dumps({'error': str(e)}), content_type='application/json')

def getProducts(request):
    return render(request, 'store/products.html')