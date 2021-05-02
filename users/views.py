from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from boards.serializers import DetailBoardSerializer
from users.models import CustomUser
from users.serializers import UsersSerializer, UsersDetailSerializer, CreateUserSerializer
from rest_framework.decorators import action


class UsersViewSet(ModelViewSet):
    User = CustomUser
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'partial_update':
            return UsersDetailSerializer
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UsersSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        return super(UsersViewSet, self).get_permissions()

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def favorites(self, request, pk=None):
        User = CustomUser
        user_detail = User.objects.get(id=pk)
        if request.method == 'GET':
            favorites = user_detail.favorites.all()
            serialized = DetailBoardSerializer(favorites, many=True)
            return Response(
                status=status.HTTP_200_OK,
                data=serialized.data)
        if request.method == 'POST':
            favoritedetail = request.data['favorite']
            for favorite in favoritedetail:
                user_detail.favorites.add(favorite)
            return Response(status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            favoritedetail = request.data['favorite']
            for favorite in favoritedetail:
                user_detail.favorites.remove(favorite)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=True)
    def creator(self, request, pk=None):
        User = CustomUser
        user_detail = User.objects.get(id=pk)
        if request.method == 'GET':
            myCreator = user_detail.creator_board.all()
            serialized=DetailBoardSerializer(myCreator,many=True)
            return Response(
                status=status.HTTP_200_OK,
                data=serialized.data
                )
