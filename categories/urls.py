from django.urls import path,include
from .views import *
urlpatterns = [
    path('categories/', category_list_create, name='category-list-create'),
    path('subcategory/', sub_category_list, name='subcategory-list-create'),
    path('products/',product_list_create,name='product-list-create'),
]
