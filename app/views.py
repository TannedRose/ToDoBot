from rest_framework import viewsets

from .models import Task, Category, User
from .serializers import TaskSerializer, CategorySerializer, UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.none()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user")
        queryset = Task.objects.select_related('category')
        if user_id:
            return queryset.filter(user_id=user_id)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
