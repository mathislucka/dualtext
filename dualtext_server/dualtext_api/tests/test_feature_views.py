from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Feature
from .factories import UserFactory, GroupFactory, CorpusFactory, FeatureFactory

class TestFeatureListView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure that registered users can view all features.
        """
        user = UserFactory()
        url = reverse('feature_list')
        feature = FeatureFactory()

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['key'], feature.key)

    def test_superuser_create(self):
        """
        Ensure that superusers can create a feature.
        """
        su = UserFactory(is_superuser=True)
        url = reverse('feature_list')
        data = {'name': 'New feature', 'key': 'feature_1'}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')

        created_feature = Feature.objects.get(id=response.data['id'])
        self.assertEqual(created_feature.key, data['key'])

    def test_deny_non_superuser_create(self):
        """
        Ensure that normal users can't create a feature
        """
        user = UserFactory()
        url = reverse('feature_list')

        self.client.force_authenticate(user=user)
        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_non_authenticated_view(self):
        """
        Ensure that non-authenticated users can't view features
        """
        url = reverse('feature_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestFeatureDetailView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure that registered users can view a single feature.
        """
        user = UserFactory()
        feature = FeatureFactory()
        url = reverse('feature_detail', args=[feature.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data['key'], feature.key)

    def test_superuser_update(self):
        """
        Ensure that superusers can update a feature.
        """
        su = UserFactory(is_superuser=True)
        feature = FeatureFactory()
        url = reverse('feature_detail', args=[feature.id])
        data = {'name': 'changed'}

        self.client.force_authenticate(user=su)
        response = self.client.patch(url, data, format='json')

        updated_feature = Feature.objects.get(id=feature.id)
        self.assertEqual(updated_feature.name, data['name'])
        self.assertEqual(response.data['id'], feature.id)

    def test_deny_non_superuser_update(self):
        """
        Ensure that non superusers users can't update a feature.
        """
        user = UserFactory()
        feature = FeatureFactory()
        url = reverse('feature_detail', args=[feature.id])
        data = {'name': 'changed'}

        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_non_authenticated_view(self):
        """
        Ensure that non-authenticated users can't view a single feature.
        """
        feature = FeatureFactory()
        url = reverse('feature_detail', args=[feature.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
