from django.urls import path, include

from .routers import api_router


urlpatterns = [
    path('', include(api_router))

]