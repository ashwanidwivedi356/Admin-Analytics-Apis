import razorpay
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from .models import Payment
from cart.models import Order
from .serializers import PaymentSerializer
from .tasks import send_order_confirmation_email
import hmac
import hashlib

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CreatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id, user=request.user)

        razorpay_order = client.order.create({
            "amount": int(order.total_price * 100),  # in paise
            "currency": "INR",
            "payment_capture": 1
        })

        payment = Payment.objects.create(
            user=request.user,
            order=order,
            amount=order.total_price,
            razorpay_order_id=razorpay_order['id']
        )

        return Response({
            "order_id": razorpay_order['id'],
            "amount": order.total_price,
            "currency": "INR",
        })

class VerifyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        generated_signature = hmac.new(
            bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
            bytes(razorpay_order_id + "|" + razorpay_payment_id, 'utf-8'),
            hashlib.sha256
        ).hexdigest()

        if generated_signature == razorpay_signature:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.is_paid = True
            payment.save()

            payment.order.status = "Delivered"
            payment.order.save()

            # Async email
            send_order_confirmation_email.delay(payment.user.email, payment.order.id)

            return Response({"message": "Payment verified successfully"}, status=200)

        return Response({"error": "Invalid payment signature"}, status=400)
