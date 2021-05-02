from django.test import TestCase

from boards.models import Board
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
        self.board1 = Board.objects.create(
            name='Tablero 1',
            description='Este es el tablero 1',
            owner=self.user
        )
        self.board2 = Board.objects.create(
            name='Tablero 2',
            description='Este es el tablero 2',
            owner=self.user
        )
        Board.objects.create(
            name='Tablero 3',
            description='Este es el tablero 3',
            owner=self.user
        )
        response = self.client.post(f'{self.host}/api/token/', {
            'email': 'newuser@gmail.com',
            'password': 'test'
        })
        self.auth = f'Bearer {response.data["access"]}'
        self.user.favorites.add(self.board1.id)

    def test_create_user(self):
        user = CustomUser
        user = user.objects.create_user(email='new@user.com', password='test2021')
        self.assertEqual(user.email, 'new@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_staff(self):
        user = CustomUser
        admin_user = user.objects.create_staff(email='staff@user.com', password='foo')
        self.assertEqual(admin_user.email, 'staff@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)

    def test_create_superuser(self):
        user = CustomUser
        admin_user = user.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_get_boards_from_a_user(self):
        response = self.client.get(f'{self.host}/users/{str(self.user.id)}/creator/')
        """response = self.client.get(f'{self.host}/users/{str(self.user.id)}/creator/', HTTP_AUTHORIZATION=self.auth)"""
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_create_favorite_boards_of_a_user(self):
        data = {'favorite': [self.board2.id]}
        response = self.client.post(f'{self.host}/users/{str(self.user.id)}/favorites/', data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_favorite_boards_of_a_user(self):
        response = self.client.get(f'{self.host}/users/{str(self.user.id)}/favorites/')
        self.assertEqual(response.status_code, 200)

    def test_create_a_favorite_boards_of_a_user(self):
        data = {'favorite': [self.board1.id]}
        response = self.client.delete(f'{self.host}/users/{str(self.user.id)}/favorites/', data, content_type="application/json")
        self.assertEqual(response.status_code, 204)
