from django.contrib import admin

from .models import Product, Category, Order, OrderProduct, Cart, Wishlist, ProductImage

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(ProductImage)