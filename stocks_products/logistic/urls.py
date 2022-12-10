from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, StockViewSet, index
from django.urls import path, include


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('stocks', StockViewSet)

#urlpatterns = router.urls
urlpatterns = [
    path('api/v1/products', include(router.urls)),
    path('api/v1/stocks', include(router.urls)),
    path('', index)
]


