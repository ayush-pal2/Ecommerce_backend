from rest_framework import serializers
from .models import Category, SubCategory, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = [
            "id",
            "category",
            "parent",
            "name",
            "is_deleted",
            "children"
        ]

    def get_children(self, obj):
        children = SubCategory.objects.filter(
            parent=obj,
            is_deleted=False
        )
        return SubCategorySerializer(children, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
