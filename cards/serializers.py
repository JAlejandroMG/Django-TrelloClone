from rest_framework.serializers import ModelSerializer
from cards.models import Card
from lists.models import List


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
            'expiration_date'
        )

    def create(self, validated_data):
        new_position = Card.objects.filter(list_id=validated_data['list_id'].id).count()+1
        card = Card(
            name=validated_data['name'],
            list_id=validated_data['list_id'],
            description=validated_data['description'],
            owner=validated_data['owner'],
            expiration_date=validated_data['expiration_date'],
            position=new_position
        )
        card.save()
        return card


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
            'members',
            'position'
        )
