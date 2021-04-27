from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date_creation = models.DateTimeField(3)
    owner = models.ForeignKey('users.User', related_name='creator_board', on_delete=models.SET_NULL, null=True)
    MEMBERS = 'MEMBERS'
    OWNER = 'OWNER'
    TYPE_CHOICES = [
        (MEMBERS, 'MEMBERS'), (OWNER, 'OWNER'),
    ]
    visibility = models.CharField(max_length=7, choices=TYPE_CHOICES, default='OWNER')
    members = models.ManyToManyField('users.User', related_name='members_board', blank=True)

    def __str__(self):
        return f'{self.name} creada por {self.owner}'
