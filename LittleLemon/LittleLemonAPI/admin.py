from django.contrib import admin
from django.conf import settings
from .models import Category, MenuItem, Order, OrderItem, Cart
# Register your models here.
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(MenuItem)


