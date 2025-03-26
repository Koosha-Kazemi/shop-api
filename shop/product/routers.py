from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet


router = SimpleRouter()


router.register(r'category', CategoryViewSet)


api_router = router.urls