

from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone

from oscar.core import compat
from oscar.apps.customer import abstract_models


class Profile(models.Model):
    user = models.OneToOneField(
        compat.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE
    )
    MALE, FEMALE = "M", "F"
    choices = ((MALE, "Male"), (FEMALE, "Female"))
    gender = models.CharField(max_length=1, choices=choices, verbose_name="Gender")
    age = models.PositiveIntegerField(verbose_name="Age")


class ExtendedUserModel(AbstractUser):
    twitter_username = models.CharField(max_length=255, unique=True)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        now = timezone.now()
        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, last_login=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        return self.create_user(email, password)

class CustomUserModel(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    twitter_username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    get_short_name = get_full_name


class ExtendedOscarUserModel(abstract_models.AbstractUser):
    twitter_username = models.CharField(max_length=255, unique=True)
