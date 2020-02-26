from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer


TAG_URL = reverse('recipe:tag-list')


class PublicTagAPITest(TestCase):
    """Test the publically available tags api"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retriving tags"""
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagAPITest(TestCase):
    """test the authorised user tags api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@vikas.com',
            'test1234'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tag(self):
        """Test that the tags for user are retrieved"""
        Tag.objects.create(user=self.user, name='Sweet')
        Tag.objects.create(user=self.user, name='Vegan')

        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by('-name')

        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returnsed are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'new@vikas.com',
            '12345678'
        )
        Tag.objects.create(user=user2, name='Butter-y')
        tag = Tag.objects.create(user=self.user, name='USER_TEST')

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Simple'}
        self.client.post(TAG_URL, payload)        

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
