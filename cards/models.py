from django.db import models

from lists.models import List
from users.models import CustomUser


class Card(models.Model):
    name = models.CharField(max_length=200)
    list_id = models.ForeignKey(
        List,
        related_name='Card',
        on_delete=models.SET_NULL,
    )
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(
        CustomUser,
        related_name='Card',
        on_delete=models.SET_NULL,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    position = models.IntegerField()
    members = models.ManyToManyField(
        CustomUser,
        related_name='Cards',
        blank=True
    )

    def __str__(self):
        return self.name
