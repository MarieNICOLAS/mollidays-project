from rest_framework import generics
from circuits.models.category import Category
from circuits.serializers.category_serializer import CategorySerializer

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True).order_by("name")
    serializer_class = CategorySerializer