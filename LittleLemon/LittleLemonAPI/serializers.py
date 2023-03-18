from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order
from django.contrib.auth.models import User

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'delivery_crew', 'status', 'total', 'date']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def united_price(self, product: Cart):
        product.unit_price = product.menuitm.price
        return product.menuitm.price

    def total_price(self, product: Cart):
        total = product.quntity * product.unit_price 
        return total

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'