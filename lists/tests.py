from rest_framework.test import APITestCase
from boards.models import Board
from lists.models import List
from users.models import CustomUser

class TestListCRUD(APITestCase):

    def setUp(self):
        User = CustomUser
        self.host = 'http://127.0.0.1:8000'
        self.user = User.objects.create(
            email ='jaime@gmail.com',
            first_name ='juan',
            last_name ='felipe',
        )
        self.board = Board.objects.create(
            id=1,
            name='List 1',
            description='This board talk about cars',
            date_creation='2021-01-01',
            owner=self.user,
            visibility='PRIVATE'
        )
        self.board = Board.objects.create(
            id=2,
            name='List 2',
            description='This board talk about cars',
            date_creation='2021-01-01',
            owner=self.user,
            visibility='PRIVATE'
        )
        for i in range(5):
            self.list = List.objects.create(
                name=f'List {i+1}',
                board_id_id=1,
                creation_date='2021-01-01',
                position=f'{i+1}'
            )
        for i in range(5):
            self.list = List.objects.create(
                name=f'List {i+5}',
                board_id_id=2,
                creation_date='2021-01-01',
                position=f'{i+5}'
            )
    def test_get_Users(self):
        response = self.client.get(f'{self.host}/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_lists(self):
        response = self.client.get(f'{self.host}/lists/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

    def test_change_position_no_exist(self):
        data = {
            'position': 3
        }
        response = self.client.patch(f'{self.host}/lists/8/position/?board=2', data)
        self.assertEqual(response.status_code, 406)

    def test_change_position(self):
        data2 = {
            'position': 4
        }
        response = self.client.patch(f'{self.host}/lists/2/position/?board=1', data2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(List.objects.get(id=2).position, data2['position'])






