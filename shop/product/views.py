from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import SAFE_METHODS

from .models import Category, Product, ProductImage
from .serializer import CategorySerializer, ProductSerializer, ProductImageSerializer

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


class ProductView(ListCreateAPIView):
    """
    Product list and creation endpoint.
    
    GET:
    Returns paginated list of all products
    
    POST:
    Create a new product instance
    
    Uses ProductSerializer for data validation and transformation
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ProductImageView(CreateAPIView):
    
    """
    Create new product images.
    
    POST /api/product-images/
    - Requires: product ID and image file
    - Returns: image details with URL
    """

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer