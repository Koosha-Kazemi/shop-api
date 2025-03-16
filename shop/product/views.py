from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializer import CategorySerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    