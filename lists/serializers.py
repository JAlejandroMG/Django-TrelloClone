from rest_framework.serializers import ModelSerializer

from lists.models import List


class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('name', 'creation_date')


class DetailListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ('name', 'creation_date', 'position')