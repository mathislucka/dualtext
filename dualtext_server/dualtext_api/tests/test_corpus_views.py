from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Corpus, Document
from .helpers import run_standard_setup

class TestCorpusListView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.url = reverse('corpus_list')
    
    def test_creation(self):
        """
        Ensure a new corpus can be created by a superuser.
        """
        data = {'name': 'Test Corpus', 'corpus_meta': { 'info': 'corpus info'}}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Corpus.objects.count(), 1)
        self.assertEqual(Corpus.objects.get(id=response.data['id']).name, 'Test Corpus')
        self.assertEqual(Corpus.objects.get(id=response.data['id']).corpus_meta, {'info': 'corpus info'})

    def test_unique_name(self):
        """
        Ensure that corpus names are unique.
        """
        data = {'name': 'Test Corpus', 'corpus_meta': { 'info': 'corpus info'}}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        response_2 = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_view(self):
        """
        Ensure a superuser can view all corpora.
        """
        corpus = Corpus(name='Foo', corpus_meta={})
        corpus.save()
        
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], corpus.name)

    def test_view_only_allowed(self):
        """
        Ensure users can only view corpora that they are allowed to see.
        """
        corpus = Corpus(name='Foo', corpus_meta={})
        corpus.save()
        corpus.allowed_groups.add(self.group)
        corpus.save()
        self.user.groups.add(self.group)
        self.user.save()
        corpus_2 = Corpus(name='Bar', corpus_meta={})
        corpus_2.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], corpus.name)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create corpora.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see corpora.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestCorpusDetailView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']

        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('corpus_detail', args=[self.corpus.id])

    def test_allowed_view(self):
        """
        Ensure that users can view a corpus that they are allowed to view.
        """
        self.corpus.allowed_groups.add(self.group)
        self.corpus.save()
        self.user.groups.add(self.group)
        self.user.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.corpus.id)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all corpora.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.corpus.id)

    def test_superuser_delete(self):
        """
        Ensure that superusers can delete a corpus.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.url, format='json')
        try:
            corpus = Corpus.objects.get(id=1)
        except Corpus.DoesNotExist:
            corpus = None

        try:
            document = Document.objects.get(id=1)
        except Document.DoesNotExist:
            document = None

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(corpus, None)
        self.assertEqual(document, None)

    def test_deny_non_member_view(self):
        """
        Ensure that users who are not allowed to view a corpus can't view it.
        """
        self.user.groups.remove(self.group)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_non_superuser_delete(self):
        """
        Ensure that users who are not superusers can't delete a corpus.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
