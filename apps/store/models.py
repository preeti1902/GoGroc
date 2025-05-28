import uuid
from django.db import models
from ..base.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User
from apps.accounts.models import Address
from django.db.models import Q

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

    def  __str__(self) -> str:
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0)
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args,**kwargs)

    def __str__(self):
        return self.name
    
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="products")

    def __str__(self):
        return self.product.name
    
class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default = 100)
    minimum_amount = models.IntegerField(default=500)
    def __str__(self) -> str:
        return self.coupon_code 

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

    def get_discount_price(self):
        return self.coupon.discount_price if self.coupon else 0

    def get_cart_total_without_discount(self):
        return sum(cart_item.total_price() for cart_item in self.cart_items.all())

    def get_cart_total(self):
        total_price = self.get_cart_total_without_discount() - self.get_discount_price()
        return max(total_price, 0)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(is_paid=False),
                name='unique_unpaid_cart_per_user'
            )
        ]

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def save(self, *args, **kwargs):
        if self.quantity < 1:
            self.delete()
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self,*args,**kwargs):
        if self.user.wishlist.filter(product=self.product).exists():
            self.delete()
        super(Wishlist, self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Order(BaseModel):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('razorpay', 'Razorpay'),
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product, through="OrderProduct")
    
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')

    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    delivery_instructions = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    order_number = models.CharField(max_length=100, unique=True, blank=True)

    def calculate_total(self):
        return sum([op.total_price() for op in self.orderproduct_set.all()])

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD{uuid.uuid4().hex[:10].upper()}"
        self.total = self.calculate_total()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.uuid} by {self.user.username} - ₹{self.total}"

class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def total_price(self):
        return self.quantity * self.price_at_order

    def save(self, *args, **kwargs):
        if not self.price_at_order:
            self.price_at_order = self.product.price
        if self.quantity < 1:
            self.delete()
        super(OrderProduct, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.user.username} - {self.product.name} ({self.quantity})"

