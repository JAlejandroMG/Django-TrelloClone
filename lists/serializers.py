from rest_framework.serializers import ModelSerializer

from boards.models import Board
from lists.models import List


class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'board_id', 'position') #Pendiente de eliminar position


class DetailListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'creation_date', 'position', 'board_id')


class AddListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('name', 'board_id')

    def create(self, validated_data):
        new_position = List.objects.filter(board_id=validated_data['board_id'].id).count()+1
        list__ = List(
            name=validated_data['name'],
            board_id=validated_data['board_id'],
            position=new_position
        )
        list__.save()
        return list__
