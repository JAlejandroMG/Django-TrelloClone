from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=200)
    list_id = models.ForeignKey(
        List,
        related_name='Card',
        on_delete=models.SET_NULL,
        null=True
    )
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User,
        related_name='Card',
        on_delete=models.SET_NULL,
        null=True
    )
    creation_date = models.DateField()
    expiration_date = models.DateField()
    position = models.IntegerField
    members = models.ManyToManyField(
        User,
        related_name='Cards',
        blank=True
    )

    def __str__(self):
        return self.name
