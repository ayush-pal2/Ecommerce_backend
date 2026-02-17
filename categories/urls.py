from django.urls import path
from .views import *

urlpatterns = [

    path('categories/', category_list_create),
    path('categories/bin/',category_bin),
    path('categories/restore/<int:pk>/',category_restore),
    path('register/',register)
]
