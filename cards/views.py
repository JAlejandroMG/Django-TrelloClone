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
    def new_position(self, request, pk=None):
        if request.method == 'PATCH':
            list_id = self.get_object().list_id.id
            card_new_position = request.data['new_position']
            if card_new_position > Card.objects.filter(list_id=list_id).count():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="No hay tal cantidad de tarjetas en la lista actual"
                )
            card_actual_position = self.get_object().position
            if card_new_position > card_actual_position:
                result = self.assign_new_positions(list_id, card_actual_position, card_new_position, '', -1)
            if card_new_position < card_actual_position:
                result = self.assign_new_positions(list_id, card_new_position, card_actual_position, '-', 1)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def assign_new_positions(self, list_id, position1, position2, order_by, change):
        try:
            if change < 0:  # card_new_position > card_actual_position
                card_to_change = Card.objects.get(list_id=list_id, position=position1)
                cards_to_modify = Card.objects.filter(list_id=list_id, position__gt=position1,
                                                      position__lte=position2).order_by(f'{order_by}position')
            else:  # card_new_position < card_actual_position
                card_to_change = Card.objects.get(list_id=list_id, position=position2)
                cards_to_modify = Card.objects.filter(list_id=list_id, position__gte=position1,
                                                      position__lt=position2).order_by(f'{order_by}position')
            card_to_change.position = -1
            card_to_change.save
            for card in cards_to_modify:
                card.position = card.position + change
                card.save()
            if change < 0:
                card_to_change.position = position2
            else:
                card_to_change.position = position1
            card_to_change.save()
            return True
        except LookupError:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
        date_to_send = expiration_date - timedelta(hours=11)
        print(date_to_send)
        send_cards_duedate_notification.apply_async(
            args=[email],
            eta=date_to_send
        )
