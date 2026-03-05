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

from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

    @classmethod
    def choices(cls):
        return [(role.value, role.name.title()) for role in cls]

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices(),
        default=UserRole.CUSTOMER.value
    )

    def is_admin(self):
        return self.role == UserRole.ADMIN.value

    def is_customer(self):
        return self.role == UserRole.CUSTOMER.value
