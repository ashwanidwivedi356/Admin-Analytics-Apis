from rest_framework import serializers
from .models import CartItem, Order, Coupon

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percent']

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'total_price', 'coupon', 'status', 'created_at']