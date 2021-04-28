from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from cards.models import Card
from cards.serializers import ShowCardsSerializer, DetailCardSerializer, AddCardSerializer


class CardsViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = ShowCardsSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve':
            return DetailCardSerializer
        if self.action == 'create':
            return AddCardSerializer
        return ShowCardsSerializer

    @action(methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'], detail=True)
    def position(self, request, pk=None):
        card = Card.objects.get(id=pk)
        card_all = Card.objects.filter(list_id=self.request.query_params['list']).order_by('-position')
        list = (self.request.query_params['list'])
        serialized = DetailCardSerializer(card)
        posicioncardamover = card.position
        request_position = int(request.data['position'])
        actual = Card.objects.get(position=request_position, list_id=list)
        if int(list) == int(serialized.data['list_id']):
            if posicioncardamover > request_position:
                for cards in card_all:
                    if posicioncardamover > cards.position > request_position:
                        new_position = Card.objects.get(position=cards.position, list_id=list)
                        position = cards.position + 1
                        new_position.position = position
                        new_position.save()
                actual.position = actual.position + 1
                actual.save()
                card.position = request_position
                card.save()
            if posicioncardamover < request_position:
                actual_position = Card.objects.get(position=request_position, list_id=list)
                card_all = Card.objects.filter(list_id=self.request.query_params['list']).order_by('position')
                for cards2 in card_all:
                    if request_position >= cards2.position > posicioncardamover:
                        new_position = Card.objects.get(position=cards2.position, list_id=list)
                        position = cards2.position - 1
                        new_position.position = position
                        new_position.save()
                card.position = request_position
                card.save()
                actual_position.position = actual_position.position - 1
                actual_position.save()
            return Response(
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
