from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category =models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    category =models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    subcategory = models.ForeignKey( SubCategory,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
