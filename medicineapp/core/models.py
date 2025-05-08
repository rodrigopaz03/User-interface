from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    auth0_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    roles = models.JSONField(default=list, blank=True)

    def has_role(self, role_name):
        return role_name in self.roles