from .models import Cart, Wishlist

def cart_items_context(request):
    cart_items = Cart.objects.none()
    cart_total = 0
    cart_item_count = 0
    unpaid_cart = None

    if request.user.is_authenticated:
        unpaid_cart = Cart.objects.filter(user=request.user, is_paid=False).first()
        if unpaid_cart:
            cart_items = unpaid_cart.cart_items.select_related("product").all()
            cart_total = unpaid_cart.get_cart_total_without_discount()
            cart_item_count = cart_items.count()

    return {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_item_count': cart_item_count,
        'unpaid_cart': unpaid_cart,
    }


def wishlist_context(request):
    wishlist_items = Wishlist.objects.none()
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product")
    return {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count()
    }