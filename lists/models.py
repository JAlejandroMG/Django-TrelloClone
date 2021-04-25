from django.db import models


class List(models.Model):
    name = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(null=True)

    def __str__(self):
        return self.title