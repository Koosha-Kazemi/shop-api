from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS

from .models import Category, Product
from .serializer import CategorySerializer, ProductSerializer

class CategoryViewSet(ModelViewSet):
    """
    A ViewSet for viewing and editing categories.
    
    Provides the following actions:
    - `list`: Retrieve all categories.
    - `create`: Add a new category.
    - `retrieve`: Fetch a single category by ID.
    - `update`: Fully update a category by ID.
    - `partial_update`: Partially update a category by ID.
    - `destroy`: Delete a category by ID.

    Uses `CategorySerializer` for all operations.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    """
    A ViewSet for managing products with separate read/write serializers.

    Supports all CRUD operations with the following behavior:
    - **Safe Methods** (GET, HEAD, OPTIONS):
      - Uses `ProductReadSerializer` for read-only operations.
    - **Unsafe Methods** (POST, PUT, PATCH, DELETE):
      - Uses `ProductWriteSerializer` for modifications.

    Actions:
    - `list`: Get all products.
    - `create`: Add a new product.
    - `retrieve`: Fetch a single product by ID.
    - `update`: Fully update a product by ID.
    - `partial_update`: Partially update a product by ID.
    - `destroy`: Delete a product by ID.
    """
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer