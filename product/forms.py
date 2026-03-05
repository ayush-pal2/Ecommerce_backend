from django import forms
from .models import Product
from categories.models import Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'price']
        

    
    