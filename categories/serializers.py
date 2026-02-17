from rest_framework import serializers
from .models import Category,User
from product.models import Product
from product.serializers import ProductSerializer

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id',
                  'name',
                  "parent",
                  "is_deleted",
                  "children",
                  "product"
                  ]
    def get_children(self,obj):
        children = Category.objects.filter(
            parent=obj,
            is_deleted = False
        )
        return CategorySerializer(children,many=True).data
    
    def get_product(self,obj):
        product= Product.objects.filter(
            category = obj,
            is_deleted = False
        )
        return ProductSerializer(product,many=True).data

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','role']
        
        def create(self,validated_data):
            user = User.objects.create(
                username = validated_data['username'],
                password = validated_data['password'],
                role = validated_data['role']
            )
            return user