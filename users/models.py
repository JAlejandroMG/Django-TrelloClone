import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    favorites = models.ManyToManyField('boards.Board', related_name='users', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


"""python manage.py makemigrations --dry-run --verbosity 3"""

""""id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"password" varchar(128) NOT NULL,
"last_login" datetime NULL,
"is_superuser" bool NOT NULL,
"first_name" varchar(30) NOT NULL,
"last_name" varchar(150) NOT NULL,
"is_staff" bool NOT NULL,
"is_active" bool NOT NULL,
"date_joined" datetime NOT NULL,
"email" varchar(254) NOT NULL UNIQUE"""
