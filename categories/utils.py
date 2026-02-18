from .models import Category
from product.models import Product

def soft_delete_category_tree(category):
    
    category.is_deleted = True
    category.save()
    
    category = Category.objects.filter(parent=category)
    
    for sub in category:
        soft_delete_category_tree(sub)
        
    

def restore_category(category):
    
    category.is_deleted = False
    category.save()
    
    category = Category.objects.filter(parent=category)
    
    for sub in category:
        restore_category(sub)
        