from django.contrib.auth.models import AbstractUser

from base.models import UUIDBaseModel


class User(UUIDBaseModel, AbstractUser):
    pass
