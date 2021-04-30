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
            'expiration_date'
        )

    def create(self, validated_data):
        data_list = validated_data['list_id']
        cards_in_list = data_list.Card
        cards_in_list_serialized = ShowCardsSerializer(cards_in_list, many=True)
        default_position_card = len(cards_in_list_serialized.data)+1
        card = Card(
            name=validated_data['name'],
            list_id=validated_data['list_id'],
            description=validated_data['description'],
            owner=validated_data['owner'],
            expiration_date=validated_data['expiration_date'],
            position=default_position_card
        )
        card.save()
        return card


class DetailCardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'list_id',
            'description',
            'owner',
            'creation_date',
            'expiration_date',
            'position',
            'members',
            'position'
        )
