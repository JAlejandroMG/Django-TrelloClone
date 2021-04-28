from rest_framework.viewsets import ModelViewSet

from comments.models import Comment
from comments.serializers import CommentSerializer, DetailCommentSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailCommentSerializer
        return CommentSerializer
