from django.test import TestCase

from users.models import CustomUser


class TestUsersManagers(TestCase):

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
