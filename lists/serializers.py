from rest_framework.serializers import ModelSerializer

from lists.models import List


class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'board_id', 'position') #Pendiente de eliminar position


class DetailListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'board_id', 'position')
