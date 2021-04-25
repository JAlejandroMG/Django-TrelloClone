from rest_framework.viewsets import ModelViewSet
from boards.models import Board
from boards.serializers import BoardSerializer


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
