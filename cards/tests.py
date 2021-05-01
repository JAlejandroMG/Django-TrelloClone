from rest_framework.test import APITestCase

from boards.models import Board
from cards.models import Card
from lists.models import List
from users.models import CustomUser


class TestCardsViewSet(APITestCase):

    def setUp(self) -> None:
        self.host = 'http://127.0.0.1:8000'
        self.user = CustomUser.objects.create(
            first_name='Chuchito',
            last_name='Pérez',
            email='cperez@gmail.com',
            password='test2021'
        )
        self.board1 = Board.objects.create(
            name="Fiesta",
            description="Preparar los festejos patronales",
            owner=self.user.id
        )
        self.list1 = List.objects.create(
            name="En espera",
            board_id=self.board1.id,
            position=len(List.objects.filter(id=self.board1.id))+1
        )
        self.card1 = Card.objects.create(
            name="Lugar",
            description="Encontrar donde hacer la fiesta",
            list_id=self.list1.id,
            owner=self.user.id,
            expiration_date="2021-04-30",
            position=len(Card.objects.filter(id=self.list1.id))+1
        )
        self.card2 = Card.objects.create(
            name="Música",
            description="Banda de música",
            list_id=self.list1.id,
            owner=self.user.id,
            expiration_date="2021-05-2",
            position=len(Card.objects.filter(id=self.list1.id))+1
        )
        self.list2 = List.objects.create(
            name="En proceso",
            board_id=self.board1.id,
            position=len(List.objects.filter(id=self.board1.id))+1
        )
        self.card3 = Card.objects.create(
            name="Promoción",
            description="Dar a conocer el evento",
            list_id=self.list2.id,
            owner=self.user.id,
            expiration_date="2021-04-30",
            position=len(Card.objects.filter(id=self.list2.id))+1
        )
        self.board2 = Board.objects.create(
            name="Convención",
            description="Arreglar preparativos de convención",
            owner=self.user.id
        )
        self.list3 = List.objects.create(
            name="En proceso",
            board_id=self.board2.id,
            position=len(List.objects.filter(id=self.board2.id))+1
        )
        self.card4 = Card.objects.create(
            name="Hospedaje",
            description="Consiguiendo precios en hoteles",
            list_id=self.list3.id,
            owner=self.user.id,
            expiration_date="2021-04-30",
            position=len(Card.objects.filter(id=self.list3.id))+1
        )
        self.card2 = Card.objects.create(
            name="Transporte",
            description="Cotizando con empresas de autobuses",
            list_id=self.list3.id,
            owner=self.user.id,
            expiration_date="2021-05-2",
            position=len(Card.objects.filter(id=self.list3.id))+1
        )

