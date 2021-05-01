from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from cards.serializers import DetailCardSerializer
from lists.models import List
from lists.serializers import ListSerializer, DetailListSerializer, AddListSerializer


class ListViewSet(ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailListSerializer
        if self.action == 'create':
            return AddListSerializer
        return ListSerializer

    @action(methods=['PATCH'], detail=True)
    def new_position(self, request, pk=None):
        if request.method == 'PATCH':
            board_id = self.get_object().board_id.id
            list_new_position = request.data['new_position']
            if list_new_position > List.objects.filter(board_id=board_id).count():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="No hay tal cantidad de listas en el tablero actual"
                )
            list_actual_position = self.get_object().position
            if list_new_position > list_actual_position:
                result = self.assign_new_positions(board_id, list_actual_position, list_new_position, '', -1)
            if list_new_position < list_actual_position:
                result = self.assign_new_positions(board_id, list_new_position, list_actual_position, '-', 1)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def assign_new_positions(self, board_id, position1, position2, order_by, change):
        try:
            if change < 0:  # list_new_position > list_actual_position
                list_to_change = List.objects.get(board_id=board_id, position=position1)
                lists_to_modify = List.objects.filter(board_id=board_id, position__gt=position1,
                                                      position__lte=position2).order_by(f'{order_by}position')
            else:    # list_new_position < list_actual_position
                list_to_change = List.objects.get(board_id=board_id, position=position2)
                lists_to_modify = List.objects.filter(board_id=board_id, position__gte=position1,
                                                      position__lt=position2).order_by(f'{order_by}position')
            list_to_change.position = -1
            list_to_change.save
            for list in lists_to_modify:
                list.position = list.position + change
                list.save()
            if change < 0:
                list_to_change.position = position2
            else:
                list_to_change.position = position1
            list_to_change.save()
            return True
        except LookupError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=True)
    def cards(self, request, pk=None):
        if request.method == 'GET':
            lists_detail = List.objects.get(id=pk)
            cards = lists_detail.Card.all()
            serialized = DetailCardSerializer(cards, many=True)
            return Response(
                status=status.HTTP_200_OK,
                data=serialized.data
            )