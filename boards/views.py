from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from boards.models import Board
from boards.serializers import BoardSerializer, DetailBoardSerializer
from lists.serializers import DetailListSerializer
from users.models import CustomUser
from users.serializers import UsersDetailSerializer


class BoardViewSet(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'partial_update':
            return DetailBoardSerializer
        return BoardSerializer

    @action(methods=['POST', 'GET'], detail=True)
    def members(self, request, pk=None):
        board = self.get_object()
        if request.method == 'POST':
            members_id = request.data['members']
            owner = CustomUser.objects.get(id=board.owner.id)
            for member_id in members_id:
                filter_data = board.members.filter(id=member_id)
                if filter_data:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
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
            serialized = UsersDetailSerializer(members, many=True)
            return Response(
                status=status.HTTP_200_OK,
                data=serialized.data
            )

    @action(methods=['GET'], detail=True)
    def lists(self, request, pk=None):
        if request.method == 'GET':
            board_detail = Board.objects.get(id=pk)
            lists = board_detail.lists.all()
            serialized = DetailListSerializer(lists, many=True)
            return Response(
                status=status.HTTP_200_OK,
                data=serialized.data
            )
