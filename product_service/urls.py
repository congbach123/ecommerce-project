from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet, ProductViewSet, 
                   BookViewSet, PhoneViewSet, ClothingViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('books', BookViewSet)
router.register('phones', PhoneViewSet)
router.register('clothing', ClothingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]