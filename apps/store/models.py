from django.db import models
from ..base.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100,null=True,blank=True)

    def get_discount_price(self):
        return self.coupon.discount_price if self.coupon else 0
    
    def get_cart_total_without_discount(self):
        total_price = sum(cart_item.get_product_price() for cart_item in self.cart_items.all())
        return total_price

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

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

class OrderProduct(BaseModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def save(self,*args,**kwargs):
        if self.quantity < 1:
            self.delete()
        super(OrderProduct, self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.order.user.username} - {self.product.name} ({self.quantity})"

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through="OrderProduct")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_completed = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        self.total = sum([product.price for product in self.products.all()])
        super(Order, self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.total}"

