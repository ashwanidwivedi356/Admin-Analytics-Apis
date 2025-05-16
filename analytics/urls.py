from django.urls import path
from .views import (
    DailyRevenueView,
    MonthlyRevenueView,
    MostSoldProductsView,
    TopCustomersView,
    OrderTrendView
)

urlpatterns = [
    path('revenue/daily/', DailyRevenueView.as_view()),
    path('revenue/monthly/', MonthlyRevenueView.as_view()),
    path('products/most-sold/', MostSoldProductsView.as_view()),
    path('customers/top/', TopCustomersView.as_view()),
    path('orders/trends/', OrderTrendView.as_view()),
]
