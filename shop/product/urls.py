from django.urls import path, include

from .routers import api_router
from .views import (
    ProductListView,
    ProductImageView,
    ProductImageDetailView,
    ProductDetailView
)

urlpatterns = [
    path('', include(api_router)),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product-image/', ProductImageView.as_view(), name='product_image'),
    path('product-image/<int:pk>/', ProductImageDetailView.as_view(), name='product_image'),
    path('product/<int:pk>',ProductDetailView.as_view(), name='product_detail')


]