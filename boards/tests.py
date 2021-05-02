from django.test import TestCase

from boards.models import Board
from lists.models import List
from users.models import CustomUser


class TestUsersManagers(TestCase):

    def setUp(self):
        self.host = 'http://127.0.0.1:8000'
        self.user = CustomUser.objects.create_user(
            email='newuser@gmail.com',
            first_name='New',
            last_name='User',
            password='test'
        )
        self.board = Board.objects.create(
            name='Tablero 1',
            description='Este es el tablero 1',
            owner=self.user
        )
        self.list = []
        for i in range(5):
            self.list.append(List.objects.create(
                name=f'List {i + 1}',
                board_id=self.board,
                creation_date='2021-01-01',
                position=f'{i + 1}'
            ))
        self.user1 = CustomUser.objects.create_user(
            email='newuser1@gmail.com',
            first_name='New',
            last_name='User',
            password='test'
        )
        self.user2 = CustomUser.objects.create_user(
            email='newuser2@gmail.com',
            first_name='New',
            last_name='User',
            password='test'
        )
        self.board.members.add(self.user1.id)
        response = self.client.post(f'{self.host}/api/token/', {
            'email': 'newuser@gmail.com',
            'password': 'test'
        })
        self.auth = f'Bearer {response.data["access"]}'

    def test_get_lists_from_a_board(self):
        response = self.client.get(f'{self.host}/boards/{str(self.board.id)}/lists/')
        """response = self.client.get(f'{self.host}/boards/{str(self.board.id)}/lists/', HTTP_AUTHORIZATION=self.auth)"""
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    def test_add_members_to_a_board(self):
        data = {'members': [self.user2.id]}
        response = self.client.post(f'{self.host}/boards/{str(self.board.id)}/members/', data, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_add_members_already_members_to_a_board(self):
        data = {'members': [self.user1.id]}
        response = self.client.post(f'{self.host}/boards/{str(self.board.id)}/members/', data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_members_from_a_board(self):
        response = self.client.get(f'{self.host}/boards/{str(self.board.id)}/members/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
