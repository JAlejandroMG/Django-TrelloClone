from rest_framework.serializers import ModelSerializer
from boards.models import Board


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'description', 'owner')


class DetailBoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'description', 'owner', 'visibility', 'members')
