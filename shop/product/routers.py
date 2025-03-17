from rest_framework.routers import SimpleRouter

from .views import CategoryView


router = SimpleRouter()


router.register(r'category', CategoryView)


api_router = router.urls