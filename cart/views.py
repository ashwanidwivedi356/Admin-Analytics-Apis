from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem, Order, Coupon
from .serializers import CartItemSerializer, OrderSerializer
from products.models import Product
from django.utils import timezone

class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RemoveCartItemView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=400)

        coupon_code = request.data.get('coupon')
        coupon = None
        discount = 0

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                if coupon.expires_at and coupon.expires_at < timezone.now():
                    return Response({"error": "Coupon expired."}, status=400)
                discount = coupon.discount_percent
            except Coupon.DoesNotExist:
                return Response({"error": "Invalid coupon code."}, status=400)

        total = sum(item.product.price * item.quantity for item in cart_items)
        total_after_discount = total * (1 - discount / 100)

        order = Order.objects.create(
            user=request.user,
            total_price=total_after_discount,
            coupon=coupon if coupon else None
        )
        order.items.set(cart_items)
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=201)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class UpdateOrderStatusView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        if not request.user.is_staff:
            return Response({"error": "Only admin can update status."}, status=403)
        status_value = request.data.get("status")
        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status."}, status=400)
        order.status = status_value
        order.save()
        return Response(OrderSerializer(order).data)
    


from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Coupon

class OrderCreateAPIView(APIView):
    def post(self, request):
        coupon_code = request.data.get("coupon")
        coupon = None

        if coupon_code:
            try:
                coupon = Coupon.objects.get(
                    code__iexact=coupon_code,
                    active=True
                )
                if coupon.expires_at and coupon.expires_at < timezone.now():
                    return Response({"error": "Coupon has expired."}, status=400)
            except Coupon.DoesNotExist:
                return Response({"error": "Invalid coupon code."}, status=400)

        # Proceed to create order...
        return Response({"message": "Order created successfully!"})
