from rest_framework.serializers import ModelSerializer

from lists.models import List


class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'board_id', 'position') #Pendiente de eliminar position


class DetailListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'creation_date', 'position','board_id')


class AddListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('name', 'board_id')

    def create(self, validated_data):
        data_board = validated_data['board_id']
        lists_in_board = data_board.lists
        lists_in_board_serialized = ListSerializer(lists_in_board, many=True)
        default_position_list = len(lists_in_board_serialized.data)+1
        list__ = List(
            name=validated_data['name'],
            board_id=validated_data['board_id'],
            position=default_position_list
        )
        list__.save()
        return list__
