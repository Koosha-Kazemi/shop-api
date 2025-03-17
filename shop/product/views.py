from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS

from .models import Category, Product
from .serializer import CategorySerializer, ProductReadSerializer, ProductWriteSerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    



class ProductView(ModelViewSet):
    queryset = Product.objects.all()


    def get_serializer_class(self):
        """
        Use ProductReadSerializer for safe methods (GET, HEAD, OPTIONS),
        and ProductWriteSerializer for unsafe methods (POST, PUT, PATCH, DELETE).
        """
        
        if self.request.method in SAFE_METHODS:
            return ProductReadSerializer
        return ProductWriteSerializer