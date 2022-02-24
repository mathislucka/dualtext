from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Corpus
from .factories import UserFactory, CorpusFactory, GroupFactory

class TestCorpusListView(APITestCase):
    def test_creation(self):
        """
        Ensure a new corpus can be created by a superuser.
        """
        su = UserFactory(is_superuser=True)
        url = reverse('corpus_list')
        data = {'name': 'Test Corpus', 'corpus_meta': { 'info': 'corpus info'}}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Corpus.objects.count(), 1)
        self.assertEqual(Corpus.objects.get(id=response.data['id']).name, 'Test Corpus')
        self.assertEqual(Corpus.objects.get(id=response.data['id']).corpus_meta, {'info': 'corpus info'})


    def test_allowed_group_create(self):
        """
        Ensure that you can set the allowed group when creating a Corpus through the API.
        """
        group = GroupFactory()

        user = UserFactory(groups=[group])
        url = reverse('corpus_list')

        su = UserFactory(is_superuser=True)
        url = reverse('corpus_list')
        data = {'name': 'Test Corpus', 'corpus_meta': {'info': 'corpus info'}, 'allowed_groups': [group.id]}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')


        self.assertEqual(Corpus.objects.get(id=response.data['id']).allowed_groups.first().name, group.name)


    def test_unique_name(self):
        """
        Ensure that corpus names are unique.
        """
        su = UserFactory(is_superuser=True)
        url = reverse('corpus_list')
        data = {'name': 'Test Corpus', 'corpus_meta': { 'info': 'corpus info'}}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')
        response_2 = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_view(self):
        """
        Ensure a superuser can view all corpora.
        """
        corpus = CorpusFactory()
        su = UserFactory(is_superuser=True)
        url = reverse('corpus_list')
        
        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], corpus.name)

    def test_view_only_allowed(self):
        """
        Ensure users can only view corpora that they are allowed to see.
        """
        group = GroupFactory()
        corpus = CorpusFactory(allowed_groups=[group])
        CorpusFactory(name='other')
        user = UserFactory(groups=[group])
        url = reverse('corpus_list')

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], corpus.name)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create corpora.
        """
        user = UserFactory()
        url = reverse('corpus_list')

        self.client.force_authenticate(user=user)
        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see corpora.
        """
        url = reverse('corpus_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestCorpusDetailView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure that users can view a corpus that they are allowed to view.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        corpus = CorpusFactory(allowed_groups=[group])
        url = reverse('corpus_detail', args=[corpus.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], corpus.id)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all corpora.
        """
        su = UserFactory(is_superuser=True)
        corpus = CorpusFactory()
        url = reverse('corpus_detail', args=[corpus.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], corpus.id)

    def test_superuser_delete(self):
        """
        Ensure that superusers can delete a corpus.
        """
        su = UserFactory(is_superuser=True)
        corpus = CorpusFactory()
        url = reverse('corpus_detail', args=[corpus.id])

        self.client.force_authenticate(user=su)
        response = self.client.delete(url, format='json')

        try:
            corpus = Corpus.objects.get(id=corpus.id)
        except Corpus.DoesNotExist:
            corpus = None

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(corpus, None)

    def test_deny_non_member_view(self):
        """
        Ensure that users who are not allowed to view a corpus can't view it.
        """
        user = UserFactory()
        corpus = CorpusFactory()
        url = reverse('corpus_detail', args=[corpus.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_non_superuser_delete(self):
        """
        Ensure that users who are not superusers can't delete a corpus.
        """
        user = UserFactory()
        corpus = CorpusFactory()
        url = reverse('corpus_detail', args=[corpus.id])

        self.client.force_authenticate(user=user)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
