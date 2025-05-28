from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import razorpay
from apnabazar import settings
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from django.core.serializers.json import DjangoJSONEncoder

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
    cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()
    coupons = Coupon.objects.all()

    if request.method == 'POST':
        if 'remove_coupon' in request.POST:
            if cart_obj:
                cart_obj.coupon = None
                cart_obj.save()
                messages.success(request, "Coupon removed successfully.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        coupon_code = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__iexact=coupon_code).first()

        if not coupon_obj:
            messages.warning(request, 'Invalid Coupon')
        elif cart_obj and cart_obj.coupon:
            messages.warning(request, 'Coupon already applied')
        elif coupon_obj.is_expired:
            messages.warning(request, 'Coupon expired')
        elif cart_obj and cart_obj.get_cart_total_without_discount() < coupon_obj.minimum_amount:
            messages.warning(request, f'Minimum amount should be Rs {coupon_obj.minimum_amount}')
        else:
            if cart_obj:
                cart_obj.coupon = coupon_obj
                cart_obj.save()
                messages.success(request, 'Coupon applied successfully.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if cart_obj:
        print("Cart Object:", cart_obj.get_cart_total())
    else:
        print("Cart Object: None")

    if cart_obj and cart_obj.cart_items.exists():
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        try:
            amount = int(float(cart_obj.get_cart_total()) * 100)
            if amount <= 0:
                messages.warning(request, "Cart total is too low to proceed with payment.")
                payment = None
            else:
                payment = client.order.create({
                    'amount': amount,
                    'currency': 'INR',
                    'payment_capture': 1
                })
                cart_obj.razor_pay_order_id = payment['id']
                cart_obj.save()
                print("Razorpay Order ID:", payment['id'])
        except Exception as e:
            messages.error(request, f"Payment gateway error: {str(e)}")
            payment = None
    else:
        messages.warning(request, 'Please Add Something to your cart')
        payment = None

    addresses = request.user.addresses.all()
    context = {
        'cart': cart_obj,
        'addresses': addresses,
        'coupons': coupons,
        'payment': payment,
    }
    return render(request, 'store/cart.html', context)

@csrf_exempt
def success(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("razorpay_order_id")
            payment_id = data.get("razorpay_payment_id")
            signature = data.get("razorpay_signature")
            address_id = data.get("address_id")
            print("Received data:", data)

            if not order_id or not address_id:
                return JsonResponse({"error": "Missing order ID or address"}, status=400)

            cart = Cart.objects.get(razor_pay_order_id=order_id)
            cart.is_paid = True
            cart.save()

            address = Address.objects.get(uuid=address_id)
            user = cart.user

            order = Order.objects.create(
                user=user,
                address=address,
                total=cart.get_cart_total(),
                payment_status='paid',
                payment_method='razorpay',
                transaction_id=payment_id
            )

            for item in cart.cart_items.all():
                OrderProduct.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_order=item.product.price
                )

            return JsonResponse({"message": "Payment successful and order created"})
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Invalid order ID"}, status=400)
        except Address.DoesNotExist:
            return JsonResponse({"error": "Invalid address ID"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

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
def removeFromCart(request, uuid):
    user = request.user
    product = get_object_or_404(Product, uuid=uuid)

    cart = Cart.objects.filter(user=user, is_paid=False).first()
    if cart:
        cart_item = cart.cart_items.filter(product=product).first()
        if cart_item:
            cart_item.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))

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
    user_orders = Order.objects.filter(user=request.user).prefetch_related('orderproduct_set__product')
    total_orders = user_orders.count()
    pending_orders = user_orders.filter(status='pending').count()
    delivered_orders = user_orders.filter(status='delivered').count()
    total_savings = 0

    orders_list = []
    for order in user_orders:
        order_products = order.orderproduct_set.all()
        product_names = ', '.join([op.product.name for op in order_products])
        savings = sum([(op.product.price - op.price_at_order) * op.quantity 
                       for op in order_products if op.product.price > op.price_at_order])
        total_savings += savings

        address_text = order.address.address if order.address else ""
        phone_number = order.address.mobile if order.address else ""

        orders_list.append({
            "id": order.order_number,
            "customer": f"{order.address.first_name} {order.address.last_name}" if order.address else "",
            "email": request.user.email,
            "product": product_names,
            "date": order.created_at.strftime("%Y-%m-%d"),
            "amount": float(order.total),
            "savings": float(savings),
            "status": order.status,
            "address": address_text,
            "phone": phone_number
        })

    context = {
        'orders_data': json.dumps(orders_list),
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'total_savings': total_savings,
    }

    return render(request, 'store/orders.html', context)


@login_required
def productOrder(request):
    return render(request, 'store/order.html')

@login_required
def addAddress(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')

        house_no = request.POST.get('house_no')
        apartment_name = request.POST.get('apartment_name')
        street_details = request.POST.get('street_details')
        landmark = request.POST.get('landmark')

        full_address = f"{house_no}, {apartment_name}, {street_details}, {landmark}"

        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        address_type = request.POST.get('address_type', 'home')

        Address.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            address=full_address,
            city=city,
            state=state,
            country="India",
            zip_code=zip_code,
            address_type=address_type
        )
        messages.success(request, "Address saved successfully!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    messages.warning(request, "Invalid request method.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))