from rest_framework.viewsets import ModelViewSet
from cards.models import Card
from cards.serializers import ShowCardsSerializer


class CardsViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = ShowCardsSerializer
