from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError(_("Superuser should have is_active as True"))
        

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser should have is_staff as True"))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser should have is_superuser as True"))
        
        return self.create_user(
            email = self.normalize_email(email),
            password = password, 
            **extra_fields,
        )

class User(AbstractUser):
    username=models.CharField(max_length=25, unique=True)
    email=models.EmailField(max_length=80, unique=True)
    phone_number = PhoneNumberField(null=False, unique=True)

     # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
         return self.email

