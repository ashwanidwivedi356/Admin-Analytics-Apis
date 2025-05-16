from django.contrib import admin
from .models import Coupon, CartItem, Order

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'active', 'expires_at')
    search_fields = ('code',)
    list_filter = ('active', 'expires_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')
    list_filter = ('user',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'coupon', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    filter_horizontal = ('items',)
