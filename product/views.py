from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

from categories.models import User,Category
from product.models import Product

from rest_framework.permissions import IsAuthenticated,AllowAny
from categories.permissions import IsAdmin
from rest_framework.decorators import permission_classes

import logging
logger = logging.getLogger(__name__)

def product_to_dict(product):
    
    return {
        "id":product.id,
        "category":product.category.id,
        "name":product.name,
        "price":product.price,
        'is_deleted':product.is_deleted
    }

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):

    logger.info("Product List requested")
    page = request.GET.get('page',1)
    limit = request.GET.get('limit',10)

    products = Product.objects.filter(
            category__is_deleted=False,is_deleted =False
        ).order_by("id")

    paginator = Paginator(products, limit)
    page_obj = paginator.get_page(page)
        
    data = [product_to_dict(prod) for prod in page_obj]
        
    return Response({
            "count": paginator.count,
            "results": list(data)
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdmin])
def product_delete(request):
    Product.objects.filter(id=request.data.get('id')).update(is_deleted=True)
    return Response({'message':'Product moved to bin'})
    


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdmin])
def product_create(request):
        name = request.data.get("name")
        price = request.data.get("price")
        category_id = request.data.get("category")
        
        category = Category.objects.filter(id=category_id).filter(is_deleted=False)
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
    
    product = Product.objects.filter(category = id).filter(is_deleted=False)
    
    if not product:
        
        return Response({"message":"product not found"},status=404)
    
    data =[product_to_dict(pro) for pro in product]
    return Response(data)
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdmin])
def update_product_com(request,id):
    
    product = Product.objects.get(id=id)
    
    if not product:
        return Response({"message":"product not found"})
    
    category_id = request.data.get("category")
    name = request.data.get("name")
    price = request.data.get("price")
    is_deleted =request.get("is_deleted")
    
    
    if not category_id and not name and not price:
        return Response({"message":"provide the full details"},status = 400)
    
    product.name=name
    product.category_id = category_id
    product.price = price
    product.is_deleted = is_deleted
    
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
    product = Product.objects.get(id=id)
    
    if not product:
        return Response({"message":"product is not found"})
    
    name = request.data.get("name")
    category = request.data.get("category")
    price = request.data.get("price")
    is_deleted=request.data.get("is_deleted")
    
    if name:
        product.name = name
    if category:
        product.category_id = category
    if price:
        product.price = price
    if is_deleted:
        product.is_deleted = is_deleted
       
    product.save() 
    logger.info("Product List updated partially")

    return Response({
        "message":"product is updated partially",
        "product":product_to_dict(product)
    })
    