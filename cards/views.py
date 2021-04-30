from datetime import timedelta, datetime

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from cards.models import Card
from cards.serializers import ShowCardsSerializer, DetailCardSerializer, AddCardSerializer
from cards.tasks import send_cards_duedate_notification
from users.models import CustomUser
from users.serializers import UsersSerializer


class CardsViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = ShowCardsSerializer

    def create(self, request):
        serialized = AddCardSerializer(data=request.data)
        if not serialized.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serialized.errors
            )
        task = serialized.save()
        user = CustomUser.objects.filter(id=task.owner.id)
        self.send_duedate_notification(user[0].email, task.expiration_date)
        return Response(
            status=status.HTTP_201_CREATED,
            data=serialized.data
        )

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve':
            return DetailCardSerializer
        if self.action == 'create':
            return AddCardSerializer
        return ShowCardsSerializer

    @action(methods=['PATCH'], detail=True)
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

    @action(methods=['GET', 'POST'], detail=True)
    def members(self, request, pk=None):
        card = self.get_object()
        if request.method == 'GET':
            members = card.members.all()
            serialized = UsersSerializer(members, many=True)
            return Response(
                status=status.HTTP_200_OK,
                data=serialized.data
            )

        if request.method == 'POST':
            list_data = card.list_id
            board_data = list_data.board_id
            members_board = board_data.members
            if members_board.filter(id=request.data['newmember']):
                member = CustomUser.objects.get(id=request.data['newmember'])
                card.members.add(member)
                send_mail(
                    'Se te asigno una tarea',
                    f'se te asigno la tarea {card.name} para el tablero {board_data.name}',
                    'trelloclone@trello.com',
                    [member.email],
                    fail_silently=False
                )
                return Response(
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    status=status.HTTP_404_NOT_FOUND
                )

    def send_duedate_notification(self, email, expiration_date) -> None:
        date_to_send = expiration_date - timedelta(days=1)
        send_cards_duedate_notification.apply_async(
            args=[email],
            eta=date_to_send
        )
