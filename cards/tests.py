from rest_framework.test import APITestCase
from boards.models import Board
from cards.models import Card
from lists.models import List
from users.models import CustomUser


class TestCardsViewSet(APITestCase):
    def setUp(self):
        user__ = CustomUser
        self.host = 'http://127.0.0.1:8000'
        self.user = user__.objects.create(
            email='jaime@gmail.com',
            first_name='juan',
            last_name='felipe',
            password='12345'
        )
        self.user02 = user__.objects.create(
            email='donovan@gamil.com',
            first_name='Donovan',
            last_name='Valencia',
            password='12345'
        )
        self.board = Board.objects.create(
            id=1,
            name='test board',
            description='solo un test de board',
            date_creation='2021-01-01',
            owner=self.user,
            visibility='PRIVATE',
        )
        self.list = List.objects.create(
            id=1,
            name='test board',
            board_id_id=1,
            creation_date='2021-01-01',
            position=1
        )
        self.cards__ = []
        for i in range(7):
            self.cards__.append(Card.objects.create(
                name=f'Card {i+1}',
                list_id_id=1,
                description=f'descripcion {i+1}',
                owner=self.user,
                creation_date='2021-01-01',
                expiration_date='2021-01-22',
                position=f'{i + 1}',
            ))
        self.members_boards = {
            'members': [str(self.user02.id)]
        }
        self.client.post(
            f'{self.host}/boards/{str(self.board.id)}/members/',
            self.members_boards,
            content_type="application/json"
        )

    def test_get_cards(self):
        response = self.client.get(f'{self.host}/cards/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)

    # def test_add_members_board(self):
    #     data_member_board = {
    #         'members': [
    #             self.user02.id,
    #             self.user.id
    #         ]
    #     }
    #
    #     response = self.client.post(f'{self.host}/boards/{str(self.board.id)}/members/', data_member_board)
    #     self.assertEqual(response.status_code, 201)
    # def test_add_members_card(self):
    #     data__ = {
    #         'newmember': self.user02.id
    #     }
    #     print(self.user02.id)
    #     print(self.cards__[1].id)
    #     response = self.client.post(f'{self.host}/cards/{str(self.cards__[1].id)}/member/', data__)
    #     self.assertEqual(response.status_code, 201)
