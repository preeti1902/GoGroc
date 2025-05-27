from .models import Cart, Wishlist

def cart_items_context(request):
    cart_items = []
    cart_total = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_paid=False).first()
        if cart:
            cart_items = cart.cart_items.select_related("product").all()
            cart_total = cart.total_price()
    return {
        'cart_items': cart_items,
        'cart_total': cart_total
    }

def wishlist_context(request):
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product")
    return {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count()
    }