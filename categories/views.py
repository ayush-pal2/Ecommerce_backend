from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

from .models import Category,User
from django.db.models import Count
from product.models import Product
from .serializers import CategorySerializer,RegisterSerializer
from .utils import *

from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
from .permissions import IsAdmin


@api_view(['GET','POST','DELETE'])
@permission_classes([AllowAny])
def category_list_create(request):
    
    if request.method == 'GET':
        page = request.GET.get('page',1)
        limit = request.GET.get('limit',5)

        categories = Category.objects.filter(is_deleted=False).filter(parent=None)
        paginator = Paginator(categories, limit)
        page_obj = paginator.get_page(page)

        serializer = CategorySerializer(page_obj, many=True)

        return Response({
            "count": paginator.count,
            "results": serializer.data
        })

    if request.method == 'POST':
        
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response({
                'message':'Only admin can create category'},
                status = status.HTTP_403_FORBIDDEN
            )
            
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        
        if not request.user.isauthenticated or request.User.role != 'admin':
            return Response({
                'message':'Only admin can DELETE category'},
                status = status.HTTP_403_FORBIDDEN
            )
        category = Category.objects.get(id=request.data.get('id'))
        soft_delete_category_tree(category)
        
        return Response({'message':'Category and all related moved to bin'})

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdmin])
def category_restore(request,pk):
    category = Category.objects.get(id=pk)
    restore_category(category)
    return Response({"message":"Category and all related restored successfully"})
    
@permission_classes([IsAuthenticated,IsAdmin])
@api_view(['GET'])
def category_bin(request):
    deleted = Category.objects.filter(is_deleted=True)
    serializer = CategorySerializer(deleted,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User registered successfully"},
                        status = status.HTTP_201_CREATED
                        )
    return Response(serializer.errors,status = 400)

