from rest_framework import serializers
from .models import Task, Category, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ["id", "title", "due_date", "category_name", "category", "user", "created_at"]

    def get_category_name(self, obj):
        return obj.category.name

    def create(self, validated_data):
        category_name = validated_data.pop("category")
        category, created = Category.objects.get_or_create(name=category_name)
        validated_data["category"] = category
        return Task.objects.create(**validated_data)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"