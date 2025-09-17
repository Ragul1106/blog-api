from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BlogViewSet

router = DefaultRouter()
router.register('blogs', BlogViewSet, basename='blogs')

urlpatterns = [
    path('api/<version>/', include(router.urls)),
]
