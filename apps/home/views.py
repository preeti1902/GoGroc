from django.shortcuts import render
from apps.store.models import Product

def  index(request):
    products = Product.objects.all()
    for product in products:
        product.original_price = product.price + product.discount if product.discount else product.price
    
    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(request.user.wishlist.all().values_list('product__uuid', flat=True))

    context = {
        'products': products,
        'wishlist_product_ids': wishlist_product_ids,
    }
    return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'about/about.html')