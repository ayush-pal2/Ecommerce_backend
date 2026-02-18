from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

from categories.models import User,Category
from .models import Product
from .serializers import ProductSerializer

from rest_framework.permissions import IsAuthenticated,AllowAny
from categories.permissions import IsAdmin
from rest_framework.decorators import permission_classes

import logging
logger = logging.getLogger(__name__)

def product_to_dict(product):
    
    return {
        "category":product.category.id,
        "name":product.name,
        "price":product.price,
        'is_deleted':product.is_deleted
    }

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def product_list(request):

    if request.method == 'GET':
        logger.info("Product List requested")
        page = request.GET.get('page',1)
        limit = request.GET.get('limit',10)

        products = Product.objects.filter(
            category__is_deleted=False
        ).order_by("id")

        paginator = Paginator(products, limit)
        page_obj = paginator.get_page(page)
        
        data = [product_to_dict(prod) for prod in page_obj]
        
        return Response({
            "count": paginator.count,
            "results": list(data)
        })
    
    if request.method == 'DELETE':
        if User.role !='admin':
            logger.warning("unauthorized attempt to delete product")
            return Response({
                'message':'only admin can DELETE product'},
                        status = status.HTTP_403_FORBIDDEN
                )
        Product.objects.filter(id=request.data.get('id').update(is_deleted = True))
        return Response({'message':'Product moved to bin'})



@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdmin])
def product_create(request):
    
    if request.method == 'POST':
        if request.user.role !='admin':
            logger.warning("unauthorized attempt to create product")
            return Response({
                'message':'only admin can create product'},
                        status = status.HTTP_403_FORBIDDEN
                    )
        name = request.data.get("name")
        price = request.data.get("price")
        category_id = request.data.get("category")
        
        category = Category.objects.filter(id=category_id).first()
        if not name and not price:
            return Response({"message":"name and price is required"},status =400)
        if not category:
            return Response({"message":"category is required"},status=400)
        
        product = Product.objects.create(
            name=name,
            price = price,
            category = category
        )
        logger.info("product created successfully")
        return Response(product_to_dict(product),status=status.HTTP_201_CREATED)


@api_view(["get"])
def get_product_by_categoryid(request,id):
    
    product = Product.objects.filter(category = id)
    
    if not product:
        
        return Response({"message":"product not found"},status=404)
    
    data =[product_to_dict(pro) for pro in product]
    return Response(data)
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdmin])
def update_product_com(request,id):
    
    if not request.user.is_authenticated or request.user.role!='admin':
            logger.warning("Unauthorized Access")
            return Response(
                {"message":"only Admin can update product"},
                status=status.HTTP_403_FORBIDDEN
            )
    product = Product.objects.get(id=id)
    
    if not product:
        return Response({"message":"product not found"})
    
    category_id = request.data.get("category")
    name = request.data.get("name")
    price = request.data.get("price")
    
    if not category_id and not name and not price:
        return Response({"message":"provide the full details"},status = 400)
    
    product.name=name
    product.category_id = category_id
    product.price = price
    
    product.save()
    logger.info("Product List updated fully")

    return Response(
        {"message":"product is update fully",
        "product":product_to_dict(product)
        }
    )
    
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated,IsAdmin])
def patch_product(request,id):
    
    if not request.user.is_authenticated or request.user.role!='admin':
            logger.warning("Unauthorized Access")
            return Response(
                {"message":"only Admin can update product"},
                status=status.HTTP_403_FORBIDDEN
                )
    
    product = Product.objects.get(id=id)
    
    if not product:
        return Response({"message":"product is not found"})
    
    name = request.data.get("name")
    category = request.data.get("category")
    price = request.data.get("price")
    
    if name:
        product.name = name
    if category:
        product.category_id = category
    if price:
        product.price = price
       
    product.save() 
    logger.info("Product List updated partially")

    return Response({
        "message":"product is updated partially",
        "product":product_to_dict(product)
    })
    