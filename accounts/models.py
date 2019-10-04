from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class ShopUser(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
