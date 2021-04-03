from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Group
from .factories import GroupFactory, UserFactory

class TestGroupListView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure that a superuser can retrieve all groups.
        """
        su = UserFactory(is_superuser=True)
        group = GroupFactory()
        url = reverse('group_list')

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], group.id)

    def test_deny_non_superuser_view(self):
        """
        Ensure that normal users can't view all groups.
        """
        user = UserFactory()
        group = GroupFactory()
        url = reverse('group_list')

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_non_read_methods(self):
        """
        Ensure that a superuser can not create a group.
        """
        su = UserFactory(is_superuser=True)
        url = reverse('group_list')

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data={}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)