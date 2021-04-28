from rest_framework.serializers import ModelSerializer

from lists.models import List


class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'board_id', 'creation_date', 'position')


class DetailListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'name', 'creation_date', 'position')
