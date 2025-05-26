from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Category, Cart, CartItem
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

@login_required
def addToCart(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)
    user = request.user
    quantity = int(request.POST.get("quantity", 1))

    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))