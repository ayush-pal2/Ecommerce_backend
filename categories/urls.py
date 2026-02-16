from django.urls import path
from .views import *

urlpatterns = [

    path('categories/', category_list_create),
    path('subcategory/', sub_category_list),
    path('products/', product_list_create),

    path('subcategory/<int:pk>/delete/', subcategory_delete),
    path('subcategory/bin/', subcategory_bin),
    path('subcategory/<int:pk>/restore/', subcategory_restore),
]
