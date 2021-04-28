from rest_framework.serializers import ModelSerializer
from cards.models import Card


class ShowCardsSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'name', 'description')


class AddCardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'name',
            'list_id',
            'description',
            'owner',
            'expiration_date',
            'expiration_date',
            'position'
        )


class DetailCardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'list_id',
            'description',
            'owner',
            'expiration_date',
            'expiration_date',
            'position',
            'members'
        )
