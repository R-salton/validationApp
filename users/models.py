from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name= models.CharField(max_length=100,blank=True, null=True)
    last_name= models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(_("password"), max_length=128, help_text="A raw password isn't stored.")
    telephone_number = models.CharField(_("telephone number"), max_length=15, unique=True, help_text="Format: +250XXXXXXXXX")
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["telephone_number"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email