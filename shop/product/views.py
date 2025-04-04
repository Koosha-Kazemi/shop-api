from optparse import OptionGroup
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import SAFE_METHODS

from .models import Category, Product, ProductImage, OptionGroup
from .serializer import (CategorySerializer, OptionGroupSerializer, 
                         ProductDetailSerializer,
                         ProductImageSerializer, 
                         ProductListSerializer)



class CategoryViewSet(ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    
    Provides full CRUD operations:
    - GET /categories/ - List all categories
    - POST /categories/ - Create new category
    - GET /categories/{id}/ - Retrieve specific category
    - PUT/PATCH /categories/{id}/ - Update category
    - DELETE /categories/{id}/ - Delete category
    
    Uses CategorySerializer for all operations.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(ListAPIView):
    """
    API endpoint for listing products with basic information.
    
    GET /products/
    - Returns paginated list of products
    - Includes only core fields (id, title, price)
    - Suitable for product listing pages
    
    Uses ProductListSerializer for optimized response structure.
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductImageView(CreateAPIView):
    """
    API endpoint for uploading product images.
    
    POST /product-images/
    - Requires multipart form data with:
      - product: ID of related product
      - image: Image file upload
      - is_main (optional): Boolean flag for primary image
    - Returns created image details with 201 status
    
    Uses ProductImageSerializer for validation and response.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductImageDetailView(RetrieveAPIView):
    """
    API endpoint for retrieving single product image details.
    
    GET /product-images/{id}/
    - Returns complete image metadata including:
      - Image URL
      - Related product ID
      - Dimensions (if available)
      - Timestamps
    
    Uses ProductImageSerializer for consistent response format.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
   


class ProductDetailView(RetrieveAPIView):
    """
    API endpoint for detailed product information.
    
    GET /products/{id}/
    - Returns complete product data including:
      - All product fields
      - Nested category information
      - Array of related images
      - Pricing details
      - Inventory status
    
    Uses ProductDetailSerializer with depth=1 for related objects.
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class OptionGroupViewSet(ModelViewSet):
    """
    API endpoint that allows option groups to be viewed or edited.
    
    Provides full CRUD operations:
    - GET /option-groups/ - List all option groups
    - POST /option-groups/ - Create new option group
    - GET /option-groups/{id}/ - Retrieve specific option group
    - PUT/PATCH /option-groups/{id}/ - Update option group
    - DELETE /option-groups/{id}/ - Delete option group
    
    Uses OptionGroupSerializer for all operations.
    """
    queryset = OptionGroup.objects.all()
    serializer_class = OptionGroupSerializer