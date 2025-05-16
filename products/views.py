from rest_framework import generics, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsAdminUserCustom
from rest_framework.permissions import IsAuthenticated

# Category CRUD (Admin only)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


# Product CRUD (Admin only)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]


# Public Product View with Filtering
class PublicProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        price_lt = self.request.query_params.get('price_lt')
        price_gt = self.request.query_params.get('price_gt')

        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if price_lt:
            queryset = queryset.filter(price__lt=price_lt)
        if price_gt:
            queryset = queryset.filter(price__gt=price_gt)

        return queryset
