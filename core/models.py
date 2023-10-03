from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from core.utils import generation_char


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


RAISON = (
    ("Cybercriminel", "Cybercriminel"),
    ("Drogue", "Drogue"),
    ("Red room", "Red room"),
    ("Trafique", "Trafique"),
    ("Autre", "Autre")
)


class DnsReclamation(models.Model):
    uri = models.CharField(max_length=255)
    raison = models.CharField(max_length=255, choices=RAISON)
    traiter = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.uri}-{generation_char()}")
        super().save(*args, **kwargs)


class Blacklist(models.Model):
    uri = models.CharField(max_length=255)
    raison = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    blacklist = models.BooleanField(default=True)


class ApprouvedDomaine(models.Model):
    uri = models.CharField(max_length=255)
    raison = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    appouved = models.BooleanField(default=True)

