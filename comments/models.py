from django.db import models
from users.models import CustomUser
from cards.models import Card


class Comment(models.Model):
    card_id = models.ForeignKey(Card, related_name="comments", on_delete=models.CASCADE)
    message = models.CharField(max_length=250)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
