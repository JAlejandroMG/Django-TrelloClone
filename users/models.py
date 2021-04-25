from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    favorites = models.ManyToManyField(
        'boards.Board',
        related_name='favorites',
        blank=True
    )
