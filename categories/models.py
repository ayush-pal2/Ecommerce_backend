from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_deleted = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        null = True,
        blank=True,
        related_name='children',
        default=None
    )
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    Role_choices =(
        ('admin','Admin'),
        ('customer','Customer')
    )
    role = models.CharField(max_length=20,choices=Role_choices,default='customer')
    
    def is_admin(self):
        return self.role =='admin'
    
    def is_customer(self):
        return self.role == 'customer'
    
    
    