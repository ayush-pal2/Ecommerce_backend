from django.db import models 
from categories.models import Category

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='products'
        )
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default = False)


    def __str__(self):
        return self.name
