from django.db import models


class List(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(null=True)

    def __str__(self):
        return self.title