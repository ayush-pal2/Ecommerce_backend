from .models import SubCategory


def soft_delete_subcategory(subcategory):

    subcategory.is_deleted = True
    subcategory.save()

    children = SubCategory.objects.filter(parent=subcategory)
    
    for child in children:
        soft_delete_subcategory(child)



def restore_subcategory(subcategory):
  
    subcategory.is_deleted = False
    subcategory.save()

    children = SubCategory.objects.filter(parent=subcategory)

    for child in children:
        restore_subcategory(child)
