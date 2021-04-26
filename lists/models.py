from django.db import models

from boards.models import Board


class List(models.Model):
    name = models.CharField(max_length=250)
    board_id = models.ForeignKey(Board, related_name='lists', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(null=True)

    def __str__(self):
        return self.name