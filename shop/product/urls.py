from django.urls import path, include

from .routers import api_router
from .views import ProductListView, ProductImageView, ProductDetailImageView, ProductDetailSerializer


urlpatterns = [
    path('', include(api_router)),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product-image/', ProductImageView.as_view(), name='product_image'),
    path('product-image/<int:pk>/', ProductDetailImageView.as_view(), name='product_image'),
    path('product/<int:pk>',ProductDetailSerializer.as_view(), name='product_detail')


]