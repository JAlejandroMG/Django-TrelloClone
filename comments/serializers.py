from rest_framework.serializers import ModelSerializer

from comments.models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class DetailCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'message', 'creation_date')
