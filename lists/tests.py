from rest_framework.test import APITestCase

from boards.models import Board
from lists.models import List


class TestListCRUD(APITestCase):

    def setUp(self):
        self.host = 'http://127.0.0.1:8000'
        self.list = List.objects.create(
            name='List 1',
            creation_date='2021-01-01',
            position='1'
        )
        self.board = Board.objects.create(
            name='List 1',
            description='This board talk about cars',
            date_creation='2021-01-01'

        )

    def test_get_lists(self):
        response = self.client.get(f'{self.host}/lists/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(self.list.id, response.data[0]['id'], response.data)

    def test_get_lists_id(self):
        response = self.client.get(f'{self.host}/lists/{self.list.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.data['name']), 'List 1')

    def test_post_lists(self):
        data = {
            'name': 'List 1',
            'creation_date': '2021-01-01',
            'position': '1'
        }

        response = self.client.post(f'{self.host}/lists/', data)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(List.objects.all().count(), 2)

    def test_delete_lists(self):
        response = self.client.delete(f'{self.host}/lists/{self.list.id}/')
        list = List.objects.all()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(list), 0)

    def test_patch_lists(self):
        data = {
            'name': 'List 2'
        }
        response = self.client.patch(f'{self.host}/lists/{self.list.id}/', data)
        list = List.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.data['name']), 'List 2')

    def test_put_lists(self):
        data = {
            'name': 'List 1',
            'creation_date': '2021-01-01',
            'position': '1',
            'board': self.board.id
        }
        response = self.client.put(f'{self.host}/lists/{self.list.id}/', data)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual((response.data['name']), 'List 2')
        self.assertEqual((response.data['creation_date']), '2021-02-01')
        self.assertEqual((response.data['position']), '1')
        self.assertEqual((response.data['board']), self.board.id)
