from rest_framework.serializers import ModelSerializer
from cards.models import Card


class ShowCardsSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'name', 'description', 'expiration_date')


class AddCardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'description',
            'list_id',
            'owner',
            'expiration_date',
            'position'
        )


class DetailCardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'description',
            'list_id',
            'owner',
            'expiration_date',
            'position',
            'members'
        )
