from .models import Category
from product.models import Product

def soft_delete_category_tree(category):
    
    category.is_deleted = True
    product = Product.objects.filter(category = category).update(is_deleted=True)
    category.save()
    
    category = Category.objects.filter(parent=category)
    
    for sub in category:
        soft_delete_category_tree(sub)
        
    
def soft_delete_category_tree(category):

    category.is_deleted = True
    category.save()

    Product.objects.filter(category=category).update(is_deleted=True)

    children = Category.objects.filter(parent=category)

    for child in children:
        soft_delete_category_tree(child)


def restore_category(category):
    
    Category.objects.filter(id=category.id).update(is_deleted=False)
    Product.objects.filter(category=category).update(is_deleted=False)
    
    category = Category.objects.filter(parent=category)
    
    for sub in category:
        restore_category(sub)
        