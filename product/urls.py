from django.urls import path
from .views import *

urlpatterns = [
    path('get', product_list),
    path('create',product_create),
    path('getbyid/<int:id>',get_product_by_categoryid),
    path('updatefull/<int:id>',update_product_com),
    path('updatepartially/<int:id>',patch_product)
]
