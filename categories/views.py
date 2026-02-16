from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

from .models import Category, SubCategory, Product
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer
from .utils import soft_delete_subcategory, restore_subcategory



@api_view(['GET','POST','DELETE'])
def category_list_create(request):

    if request.method == 'GET':
        page = request.GET.get('page',1)
        limit = request.GET.get('limit',5)

        categories = Category.objects.all()
        paginator = Paginator(categories, limit)
        page_obj = paginator.get_page(page)

        serializer = CategorySerializer(page_obj, many=True)

        return Response({
            "count": paginator.count,
            "results": serializer.data
        })

    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        category = Category.objects.get(id=request.data.get('id'))
        category.delete()
        return Response({'message':'Category deleted successfully'})
    
        



@api_view(['GET','POST'])
def sub_category_list(request):

    if request.method == 'GET':
        page = request.GET.get('page',1)
        limit = request.GET.get('limit',5)

        subcats = SubCategory.objects.filter(is_deleted=False)
        paginator = Paginator(subcats, limit)
        page_obj = paginator.get_page(page)

        serializer = SubCategorySerializer(page_obj,many=True)

        return Response({
            "count": paginator.count,
            "results": serializer.data
        })

    if request.method == 'POST':
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','POST'])
def product_list_create(request):

    if request.method == 'GET':
        page = request.GET.get('page',1)
        limit = request.GET.get('limit',10)

        products = Product.objects.filter(
            subcategory__is_deleted=False
        )

        paginator = Paginator(products, limit)
        page_obj = paginator.get_page(page)

        serializer = ProductSerializer(page_obj,many=True)

        return Response({
            "count": paginator.count,
            "results": serializer.data
        })

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def subcategory_delete(request, pk):
    subcat = SubCategory.objects.get(id=pk)
    soft_delete_subcategory(subcat)
    return Response({"message":"Moved to bin"})


@api_view(['GET'])
def subcategory_bin(request):
    deleted = SubCategory.objects.filter(is_deleted=True)
    serializer = SubCategorySerializer(deleted,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def subcategory_restore(request, pk):
    subcat = SubCategory.objects.get(id=pk)
    restore_subcategory(subcat)
    return Response({"message":"Restored successfully"})
