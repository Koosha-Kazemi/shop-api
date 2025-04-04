from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, OptionGroupViewSet


router = SimpleRouter()


router.register(r'category', CategoryViewSet)
router.register(r'option-group', OptionGroupViewSet)


api_router = router.urls