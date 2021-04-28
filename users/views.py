from rest_framework.viewsets import ModelViewSet

from users.models import CustomUser
from users.serializers import UsersSerializer, UsersDetailSerializer


class UsersViewSet(ModelViewSet):
    User = CustomUser
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UsersDetailSerializer
        return UsersSerializer
