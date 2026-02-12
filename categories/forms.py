from typing import Text
from django import forms
from django.forms import fields, models, widgets
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
        
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields =['category','name']
        
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =['category','subcategory','name','price']
        
