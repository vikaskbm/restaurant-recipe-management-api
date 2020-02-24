from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """these tests would not require authernications"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid credentials/ payload"""
        payload = {
            'email': 'test@vikas.com',
            'password': 'test1234',
            'name': 'Test Case'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        us = get_user_model().objects.get(**res.data)
        self.assertTrue(
            us.check_password(payload['password'])
        )

        self.assertNotIn('password', res.data)

    def test_user_already_exists(self):
        """Test that checks if the user already exists in database"""

        payload = {
            'email': 'test@vikas.com',
            'password': 'test1234'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """"The password must be greater than 5 character"""

        payload = {
            'email': 'test@vikas.com',
            'password': 'test'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
    	"""Test that a token is created for a new user"""
    	payload = {
    		'email': 'test@vikaskbm@gmail.com',
    		'password': 'test1234'
    	}

    	create_user(**payload)
    	res = self.client.post(TOKEN_URL, payload)
    	self.assertIn('token', res.data)
    	self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
    	"""Test that token not created when invalid credentials given"""
    	create_user(email='test@vikas.com', password='test1234')
    	payload = {
    		'email': 'test@vikas.com',
    		'password': 'test'
    	}

    	res = self.client.post(TOKEN_URL, payload)
    	self.assertNotIn('token', res.data)
    	self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
    	""""Test that token not created is user doesn't exist"""
    	payload = {
    		'email': 'test@vikas.com',
    		'password': 'test1234'
    	}

    	res = self.client.post(TOKEN_URL, payload)
    	self.assertNotIn('token', res.data)
    	self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
    	"""Test that email and password are required"""
    	res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
    	self.assertNotIn('token', res.data)
    	self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
