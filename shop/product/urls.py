from django.urls import path, include

from .routers import api_router
from .views import ProductView


urlpatterns = [
    path('', include(api_router)),
    path('product/', ProductView.as_view(), name='product_list')

]