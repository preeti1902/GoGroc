from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, Category, Cart, CartItem, Wishlist, Coupon
from django.contrib import messages
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

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(request.user.wishlist.all().values_list('product__uuid', flat=True))

    context = {
        'products': products,
        'categories': category,
        'wishlist_product_ids': wishlist_product_ids,
    }
    return render(request, 'store/products.html', context)

@login_required
def cartPage(request):
    cart_obj = None
    try:
        cart_obj = Cart.objects.get(is_paid=False, user=request.user)
    except Exception as e:
        print(e)
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)
        
        if not coupon_obj.exists():
            messages.warning(request, 'Coupon Invalid')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.coupon:
            messages.warning(request, 'Coupon Already Exist')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request, f'Amount should be greater than {coupon_obj[0].minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj[0].is_expired:
            messages.warning(request, 'Coupon Expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
             
        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, 'Coupon Applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'cart': cart_obj}
    return render(request, 'store/cart.html', context)

@login_required
def dashboard(request):
    user = request.user
    cart = Cart.objects.filter(user=user, is_paid=False).first()
    
    if not cart:
        return render(request, 'store/dashboard.html', {'cart': None})

    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'store/dashboard.html', context)

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

@login_required
def addToWishlist(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)
    user = request.user

    wishlist_item = Wishlist.objects.filter(user=user, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(user=user, product=product)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def orderPage(request):
    return render(request, 'store/orders.html')

@login_required
def productOrder(request):
    return render(request, 'store/order.html')