from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum, Count
from django.utils.timezone import now
from datetime import timedelta
from cart.models import Order, CartItem
from user.models import User
from products.models import Product
from payments.models import Payment

class DailyRevenueView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = now().date()
        orders = Order.objects.filter(created_at__date=today)
        revenue = orders.aggregate(total=Sum('total_price'))['total'] or 0
        return Response({"date": today, "revenue": revenue})


class MonthlyRevenueView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = now().date()
        start_date = today.replace(day=1)
        orders = Order.objects.filter(created_at__date__gte=start_date)
        revenue = orders.aggregate(total=Sum('total_price'))['total'] or 0
        return Response({"month": today.strftime("%B"), "revenue": revenue})


class MostSoldProductsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        product_sales = (
            CartItem.objects.values('product__name')
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')[:5]
        )
        return Response(product_sales)


class TopCustomersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        top_customers = (
            Order.objects.values('user__email')
            .annotate(total_spent=Sum('total_price'))
            .order_by('-total_spent')[:5]
        )
        return Response(top_customers)


class OrderTrendView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        last_7_days = now().date() - timedelta(days=7)
        trends = (
            Order.objects.filter(created_at__date__gte=last_7_days)
            .extra({'day': "date(created_at)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        return Response(trends)
