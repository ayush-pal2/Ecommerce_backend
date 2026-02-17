from django.urls import path
from .views import *

urlpatterns = [
    path('create', product_list_create),
]
