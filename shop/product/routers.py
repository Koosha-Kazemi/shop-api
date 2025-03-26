from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, ProductViewSet


router = SimpleRouter()


router.register(r'category', CategoryViewSet)
router.register(r'prodct', ProductViewSet)


api_router = router.urls