from rest_framework.routers import SimpleRouter

from .views import CategoryView


router = SimpleRouter()


router.registry(r'category', CategoryView)


api_router = router.urls