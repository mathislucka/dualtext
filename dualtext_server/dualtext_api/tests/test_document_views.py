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
