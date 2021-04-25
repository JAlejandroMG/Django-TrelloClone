from rest_framework.serializers import ModelSerializer


class UsersSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email')


class UsersDetailSerializer:
    class Meta:
        fields = ('first_name', 'last_name', 'email')
