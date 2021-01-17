from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Document, Corpus
from .helpers import run_standard_setup

class TestDocumentListView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        
        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('document_list', args=[self.corpus.id])

    def test_allowed_view(self):
        """
        Ensure that users can view documents that they are allowed to view.
        """
        self.corpus.allowed_groups.add(self.group)
        self.corpus.save()
        self.user.groups.add(self.group)
        self.user.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], self.document.content)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all documents.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], self.document.content)

    def test_superuser_create(self):
        """
        Ensure that superusers can create new documents.
        """
        data = {'content': 'A new document'}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], data['content'])

    def test_deny_non_superuser_create(self):
        """
        Ensure that non superusers can not create new documents.
        """
        data = {'content': 'A new document'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see documents.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestDocumentDetailView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']

        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('document_detail', args=[self.document.id])

    def test_allowed_view(self):
        """
        Ensure that users can view documents that they are allowed to view.
        """
        self.corpus.allowed_groups.add(self.group)
        self.corpus.save()
        self.user.groups.add(self.group)
        self.user.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.document.content)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all documents.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.document.content)

    def deny_not_allowed_view(self):
        """
        Ensure that users can only view a document that they are allowed to view.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestDocumentBatchCreateView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        
        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        self.url = reverse('document_batch_create', args=[self.corpus.id])

    def test_superuser_create(self):
        """
        Ensure that superusers can create a batch of documents.
        """
        data = []
        n = 20
        while n > 0:
            data.append({'content': 'document {}'.format(n)})
            n -= 1
 
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 20)

    def test_batch_limited(self):
        """
        Ensure that a batch is limited to 200 documents.
        """
        data = []
        n = 201
        while n > 0:
            data.append({'content': 'document {}'.format(n)})
            n -= 1
 
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deny_non_superuser_create(self):
        """
        Ensure that non superusers can not create new documents.
        """
        data = [{'content': 'A new document'}]
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

