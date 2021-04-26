from rest_framework.serializers import ModelSerializer

from users.models import User


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UsersDetailSerializer:
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
