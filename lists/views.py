from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
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
    def position(self, request, pk=None):
        if request.method == 'PATCH':
            # selecciono la lista  a mover por el id
            list = List.objects.get(id=pk)
            # seleccionamos las listas pertenecientes a un board
            list_all = List.objects.filter(board_id=self.request.query_params['board']).order_by('-position')
            # establecemos el board para las validaciones
            board = (self.request.query_params['board'])
            serialized = DetailListSerializer(list)
            # encontramos la posicion de la lista a mover
            posicionlistaamover = list.position
            # valor de posicion a donde queremos mover la lista, que es enviado en el request
            request_position = int(request.data['position'])
            # valor de posicion de la lista a donde vamos a mover
            actual = List.objects.get(position=request_position, board_id=board)
            # verificacion de que la lista seleccionada por id pertenezca al tablero
            if int(board) == int(serialized.data['board_id']):
                # algoritmo para cuando se mueve la lista de una posicion mayor a menor
                if posicionlistaamover > request_position:
                    for lists in list_all:
                        if posicionlistaamover > lists.position > request_position:
                            new_position = List.objects.get(position=lists.position, board_id=board)
                            position = lists.position + 1
                            new_position.position = position
                            new_position.save()
                    actual.position = actual.position + 1
                    actual.save()
                    list.position = request_position
                    list.save()
                    # algoritmo para cuando se mueve la lista de una posicion menor a una mayor
                if posicionlistaamover < request_position:
                    actual_position = List.objects.get(position=request_position, board_id=board)
                    list_all = List.objects.filter(board_id=self.request.query_params['board']).order_by('position')
                    for lists2 in list_all:
                        if request_position >= lists2.position > posicionlistaamover:
                            new_position = List.objects.get(position=lists2.position, board_id=board)
                            position = lists2.position - 1
                            new_position.position = position
                            new_position.save()
                    list.position = request_position
                    list.save()
                    actual_position.position = actual_position.position - 1
                    actual_position.save()
                return Response(
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )