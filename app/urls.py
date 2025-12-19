from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from app.views import TaskViewSet, CategoryViewSet, UserViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
