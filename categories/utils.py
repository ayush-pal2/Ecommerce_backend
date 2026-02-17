from .models import Category
from product.models import Product

def soft_delete_category_tree(category):
    
    category = Category.objects.filter(category=category)
    
    for sub in category:
        soft_delete_category_tree(sub)
        
    category.is_deleted = True
    category.save()

def restore_category(category):
    
    category = Category.objects.filter(category=category)
    
    for sub in category:
        restore_category(sub)
        
    category.is_deleted = False
    category.save()