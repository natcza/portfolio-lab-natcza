from django.db import models

# Create your models here.
"""Declare models for my accounts app."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

"""Import for create a custom Manger for the new User model"""
from django.contrib.auth.models import AbstractUser, BaseUserManager  # a new class is imported

"""Create a custom Manager for the new User model.
Because my User model has one filed less than the Django original, it is important to modify its manager and make sure
it doesn't make use of the username field.
"""


class UserManger(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password"""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model"""
    username = None #Dajngo uwaza, ze pole zostalo usuneite bo nie jest instancja klasy models
    email = models.EmailField(_('email address'), unique=True) #funkcja od tlumaczen

    USERNAME_FIELD = 'email'  #polem logowania jest teraz email
    REQUIRED_FIELDS = []      #do czego sluzy REQUIRED_FIELDS? dlaczego powinno byc puste

    objects = UserManger()
