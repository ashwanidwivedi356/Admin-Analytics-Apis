from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    ProductListCreateView, ProductDetailView,
    PublicProductListView
)

urlpatterns = [
    # Category
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),

    # Product
    path('products/', ProductListCreateView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),

    # Public access
    path('store/products/', PublicProductListView.as_view()),
]
