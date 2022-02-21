from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Document
from .factories import UserFactory, GroupFactory, CorpusFactory, DocumentFactory

class TestDocumentListView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure that users can view documents that they are allowed to view.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        corpus = CorpusFactory(allowed_groups=[group])
        document = DocumentFactory(corpus=corpus)
        url = reverse('document_list', args=[corpus.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], document.content)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all documents.
        """
        su = UserFactory(is_superuser=True)
        document = DocumentFactory()
        url = reverse('document_list', args=[document.corpus.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], document.content)

    def test_superuser_create(self):
        """
        Ensure that superusers can create new documents.
        """
        su = UserFactory(is_superuser=True)
        corpus = CorpusFactory()
        url = reverse('document_list', args=[corpus.id])
        data = {'content': 'A new document'}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], data['content'])

    def test_deny_non_superuser_create(self):
        """
        Ensure that non superusers can not create new documents.
        """
        user = UserFactory()
        corpus = CorpusFactory()
        url = reverse('document_list', args=[corpus.id])
        data = {'content': 'A new document'}

        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_meta_field(self):
        """
        Ensure that a document accepts meta data in a meta field.
        """
        user = UserFactory(is_superuser=True)
        corpus = CorpusFactory()
        url = reverse('document_list', args=[corpus.id])
        data = {'content': 'A new document', 'document_meta': {'doc_id': 'external-doc-id'}}

        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.data['document_meta'], data['document_meta'])

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see documents.
        """
        corpus = CorpusFactory()
        url = reverse('document_list', args=[corpus.id])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestDocumentDetailView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure that users can view documents that they are allowed to view.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        corpus = CorpusFactory(allowed_groups=[group])
        doc = DocumentFactory(corpus=corpus)
        url = reverse('document_detail', args=[doc.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], doc.content)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all documents.
        """
        su = UserFactory(is_superuser=True)
        doc = DocumentFactory()
        url = reverse('document_detail', args=[doc.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], doc.content)

    def deny_not_allowed_view(self):
        """
        Ensure that users can only view a document that they are allowed to view.
        """
        user = UserFactory()
        doc = DocumentFactory()
        url = reverse('document_detail', args=[doc.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestDocumentBatchView(APITestCase):
    def test_superuser_create(self):
        """
        Ensure that superusers can create a batch of documents.
        """
        su = UserFactory(is_superuser=True)
        corpus = CorpusFactory()
        url = reverse('document_batch', args=[corpus.id])

        data = []
        n = 20
        while n > 0:
            data.append({'content': 'document {}'.format(n)})
            n -= 1

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 20)
        self.assertEqual(len(Document.objects.all()), 20)

    def test_batch_limited(self):
        """
        Ensure that a batch is limited to 200 documents.
        """
        su = UserFactory(is_superuser=True)
        corpus = CorpusFactory()
        url = reverse('document_batch', args=[corpus.id])

        data = []
        n = 201
        while n > 0:
            data.append({'content': 'document {}'.format(n)})
            n -= 1
 
        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deny_non_superuser_create(self):
        """
        Ensure that non superusers can not create new documents.
        """
        user = UserFactory()
        corpus = CorpusFactory()
        url = reverse('document_batch', args=[corpus.id])
        data = [{'content': 'A new document'}]

        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
