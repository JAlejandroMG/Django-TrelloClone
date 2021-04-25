from rest_framework.serializers import ModelSerializer
from cards.models import Card


class ShowCardsSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'name', 'description')
