from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    """docstring for AdminSiteTest"""
    # 1.Create setup function -> a function that runs before every other test

    def setUp(self):
        """will create our test client, add a new user to test, make sure the
        user is logged in and make a new user that is not authenticated"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@vikas.com',
            password='admin1234'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='test@vikas.com',
            password='test1234',
            name='Test User full name'
        )

    def test_users_listed(self):
        """test that the users are listed in user admin page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_users_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test that create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
