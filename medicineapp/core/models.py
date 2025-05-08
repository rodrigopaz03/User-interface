from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):

    
    class Meta:

        swappable = 'AUTH_USER_MODEL'

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='core_user_groups', 
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='core_user_permissions', 
        related_query_name='user',
    )
    class Meta:
        # Evita conflictos con el modelo auth.User
        swappable = 'AUTH_USER_MODEL'