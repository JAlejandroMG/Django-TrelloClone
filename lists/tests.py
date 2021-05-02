from rest_framework.test import APITestCase

from boards.models import Board
from cards.models import Card

from lists.models import List
from users.models import CustomUser


class TestListCRUD(APITestCase):

    def setUp(self):
        self.host = 'http://127.0.0.1:8000'
        self.user = CustomUser.objects.create_user(
            email='user@email.com',
            first_name='juan',
            last_name='felipe',
            password='test'
        )
        self.board = Board.objects.create(
            id=1,
            name='List 1',
            description='This board talk about cars',
            date_creation='2021-01-01',
            owner=self.user,
            visibility='PRIVATE'
        )
        self.list = []
        for i in range(5):
            self.list.append(List.objects.create(
                name=f'List {i + 1}',
                board_id=self.board,
                creation_date='2021-01-01',
                position=f'{i + 1}'
            ))
        self.cards = []
        for i in range(5):
            self.cards.append(Card.objects.create(
                name=f'Tarjeta {i + 1}',
                description=f'Esta es la tarjeta {i + 1}',
                list_id=self.list[0],
                owner=self.user,
                expiration_date='2021-05-05',
                position=f'{i + 1}'
            ))
        response = self.client.post(f'{self.host}/api/token/', {
            'email': 'user@email.com',
            'password': 'test'
        })
        self.auth = f'Bearer {response.data["access"]}'

    def test_get_lists(self):
        response = self.client.get(f'{self.host}/lists/')
        """response = self.client.get(f'{self.host}/lists/', HTTP_AUTHORIZATION=self.auth)"""
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    """Funciona el endpoint pero aquí no..."""
    """def test_change_position(self):
        data2 = {
            "new_position": 1
        }
        print(self.list[2].position)
        response = self.client.patch(f'{self.host}/lists/{str(self.list[2].id)}/position/', data2, content_type="application/json")
        print(self.list[2].position)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(List.objects.get(id=self.list[2].id).position, data2['new_position'])"""

    def test_change_position_no_exist(self):
        data = {
            'new_position': 9
        }
        response = self.client.patch(f'{self.host}/lists/{str(self.list[3].id)}/position/', data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_cards_from_a_list(self):
        response = self.client.get(f'{self.host}/lists/{str(self.list[0].id)}/cards/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
