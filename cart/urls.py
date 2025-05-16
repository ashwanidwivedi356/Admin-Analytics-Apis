from django.urls import path
from .views import (
    CartItemView,
    RemoveCartItemView,
    CreateOrderView,
    OrderListView,
    UpdateOrderStatusView
)

urlpatterns = [
    path('cart/', CartItemView.as_view(), name='cart'),
    path('cart/remove/<int:pk>/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    path('order/create/', CreateOrderView.as_view(), name='create-order'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('order/status/<int:pk>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]