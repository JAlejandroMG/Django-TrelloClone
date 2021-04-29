from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from boards.models import Board
from boards.serializers import BoardSerializer, DetailBoardSerializer
from users.models import CustomUser


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'partial_update':
            return DetailBoardSerializer
        return BoardSerializer

    @action(methods=['POST','GET'], detail=True)
    def members(self, request, pk=None):
        board = self.get_object()
        if request.method == 'POST':
            members_id = request.data['members']
            owner = CustomUser.objects.get(email=board.owner)
            for member_id in members_id:
                member = CustomUser.objects.get(id=member_id)
                board.members.add(member)
                send_mail(
                    'Nuevo miembro tablero Trello',
                    f'{owner.first_name} {owner.last_name} te incluido al tablero {board.name}',
                    'trelloclone@trello.com',
                    [member.email],
                    fail_silently=False
                )
            return Response(status=status.HTTP_201_CREATED)

        board_detail = Board.objects.get(id=pk)
        if request.method == 'GET':
            members = board_detail.members.all()
            serialized = DetailBoardSerializer(members)
            return Response(
                status=status.HTTP_200_OK,
                data=serialized.data
            )