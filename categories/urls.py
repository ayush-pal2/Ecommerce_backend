from django.urls import path
from .views import *

urlpatterns = [
    path('get/', category_list),
    path('getbyid/<int:id>',category_by_id),
    path('create',category_create),
    path('putcategory/<int:id>',put_category_create),
    path('patchcategory/<int:id>',category_update_patch),
    path('delete',category_delete),
    path('bin/',category_bin),
    path('restore/',category_restore),
    path('register/',register)
]
