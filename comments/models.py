from django.db import models


class Comment(models.Model):
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
