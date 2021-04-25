from django.db import models


class Comment(models.Model):
    message = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
