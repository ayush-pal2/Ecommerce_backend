from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

from categories.models import User
from .models import Product
from .serializers import ProductSerializer

from rest_framework.permissions import IsAuthenticated,AllowAny
from categories.permissions import IsAdmin
from rest_framework.decorators import permission_classes

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def product_list_create(request):

    if request.method == 'GET':
        page = request.GET.get('page',1)
        limit = request.GET.get('limit',10)

        products = Product.objects.filter(
            category__is_deleted=False
        )

        paginator = Paginator(products, limit)
        page_obj = paginator.get_page(page)

        serializer = ProductSerializer(page_obj,many=True)

        return Response({
            "count": paginator.count,
            "results": serializer.data
        })

    if request.method == 'POST':
        
        if User.role !='admin':
            return Response({
                'message':'only admin can create product'},
                        status = status.HTTP_403_FORBIDDEN
                    )
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        if User.role !='admin':
            return Response({
                'message':'only admin can DELETE product'},
                        status = status.HTTP_403_FORBIDDEN
                )
        Product.objects.filter(id=request.data.get('id').update(is_deleted = True))
        return Response({'message':'Product moved to bin'})
