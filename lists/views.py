from rest_framework.viewsets import ModelViewSet

from lists.models import List
from lists.serializers import ListSerializer, DetailListSerializer


class ListViewSet(ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailListSerializer
        return ListSerializer
