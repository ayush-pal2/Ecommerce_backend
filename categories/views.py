from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

from categories.models import Category,User
from django.db.models import Count
from product.models import Product

from .utils import *

from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
from .permissions import IsAdmin

import logging
logger = logging.getLogger(__name__)

def category_to_dict(category):
    children = Category.objects.filter(
        parent=category,
        is_deleted=False
    )
    return {
        "id":category.id,
        "name":category.name,
        "parent":category.parent.id if category.parent else None,
        'is_deleted':category.is_deleted,
        "children": [category_to_dict(child) for child in children]
    }

@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    
    if request.method == 'GET':
        logger.info("Category List requested")
        page = request.GET.get('page',1)
        limit = request.GET.get('limit',5)

        categories = Category.objects.filter(is_deleted=False, parent=None).order_by("id")
        paginator = Paginator(categories, limit)
        page_obj = paginator.get_page(page)
        
        data = [category_to_dict(cat) for cat in page_obj]

        return Response({
            "count": paginator.count,
            "results": list(data)
        })



@api_view(['POST'])
@permission_classes([IsAdmin,IsAuthenticated])
def category_create(request):
    if request.method == 'POST':
        
        if not request.user.is_authenticated or request.user.role != 'admin':
            logger.warning("unauthorized attempt to create category")
            return Response(
                {'message':'Only admin can create category'},
                status = status.HTTP_403_FORBIDDEN
            )
            
        name = request.data.get("name")
        parent_id = request.data.get("parent")
        
        if not name:
            return Response({"message":"name is required"},status =400)
        
        parent = None
        if parent_id:
            parent = Category.objects.get(id=parent_id)
        
        category = Category.objects.create(
            name = name,
            parent = parent
        )
        
        logger.warning("category creation failed dure to invalid data ")
        return Response(category_to_dict(category),status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAdmin,IsAuthenticated])
def put_category_create(request,id):
    
    if not request.user.is_authenticated or request.user.role!='admin':
            logger.warning("Unauthorized Access")
            return Response(
                {"message":"only Admin can update category"},
                status=status.HTTP_403_FORBIDDEN
            )
    category = Category.objects.filter(id=id).first()
    
    if not category:
        return Response({"message":"category not found"})
    
    name = request.data.get("name")
    parent_id = request.data.get("parent")
    
    if not name:
        return Response(
            {"message":"name is required"},
            status = 400
        )
    category.name=name
    category.parent_id = parent_id
    
    category.save()
    logger.info("category updated fully")
    return Response(
        {
            "message":"Category updated successfully",
            "categroy":category_to_dict(category)
        }
    )
    
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdmin])
def category_update_patch(request, id):
    
    if not request.user.is_authenticated or request.user.role!='admin':
            logger.warning("Unauthorized Access")
            return Response(
                {"message":"only Admin can update category"},
                status=status.HTTP_403_FORBIDDEN
        )
    category = Category.objects.filter(id=id).first()
    if not category:
        return Response({"message": "Category not found"}, status=404)

    if "name" in request.data:
        category.name = request.data.get("name")

    if "parent" in request.data:
        category.parent_id = request.data.get("parent")

    category.save()
    logger.info("category is update partially")
    return Response({
        "message": "Category partially updated",
        "category": category_to_dict(category)
    })



@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdmin])
def category_delete(request):
    if request.method == "DELETE":
        
        if not request.user.is_authenticated or request.user.role!='admin':
            logger.warning("Unauthorized Access")
            return Response(
                {"message":"only Admin can delete category"},
                status=status.HTTP_403_FORBIDDEN
            )
        category = Category.objects.get(id=request.data.get('id'))
        soft_delete_category_tree(category)
        logger.warning("category and related items moved to bin")
        return Response({'message':'Category and all related moved to bin'})
        
        

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdmin])
def category_restore(request):

    category_id = request.data.get("id")

    if not category_id:
        return Response({"error": "id is required"}, status=400)

    category = Category.objects.get(id=category_id)
    restore_category(category)

    logger.info("category restored")

    return Response({"message": "Category restored successfully"})
    
    

@permission_classes([IsAuthenticated,IsAdmin])
@api_view(['GET'])
def category_bin(request):
    deleted = Category.objects.filter(is_deleted=True)
    data = [category_to_dict(cat) for cat in deleted]
    
    logger.info("deleted category list requested")
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def category_by_id(request,id):
    logger.info("Category List requested")
                
    category = Category.objects.filter(id=id).first()
        
    if not category:
        return Response({"message": "Category not found"}, status=404)
    
    return Response(category_to_dict(category))

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {"message":"username and passowrd is required"},
            status = 400
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {"error":"user already exists"},
            status = 400
        )
        
    user = User.objects.create(
        username=username,
        password = password
    )
    logger.info("user is registered")
    
    return Response(
        {"message":"User registered Successfully"},
        status = status.HTTP_201_CREATED
    )
    
