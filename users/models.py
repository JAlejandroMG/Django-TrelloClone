from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    favorites = models.ManyToManyField('boards.Board', related_name='users', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
