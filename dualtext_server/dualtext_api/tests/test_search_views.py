from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .factories import DocumentFactory, UserFactory, TaskFactory, ProjectFactory, AnnotationFactory

class TestSearchView(APITestCase):    
    def test_elasticsearch_results(self):
        """
        Ensure the search with elasticsearch will return all matching documents in a corpus.
        """
        su = UserFactory(is_superuser=True)
        doc = DocumentFactory(content='a new document')
        url = reverse('search')
        query = '?query=document&corpus={}&method=elastic'.format(doc.corpus.id)

        self.client.force_authenticate(user=su)
        response = self.client.get(url + query, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['content'], doc.content)

    def test_deny_not_authenticated(self):
        """
        Ensure the search can only be used by authenticated users.
        """
        url = reverse('search')
        response = self.client.get(url + '?query=document&corpus=1&method=elastic', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deny_non_member(self):
        """
        Ensure that a user only gets results from a corpus if they are in the allowed_groups.
        """
        user = UserFactory()
        doc = DocumentFactory(content='a new document')
        url = reverse('search')
        query = '?query=document&corpus={}&method=elastic'.format(doc.corpus.id)

        self.client.force_authenticate(user=user)
        response = self.client.get(url + query, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_no_results_incomplete_params(self):
        """
        Ensure that no results are returned if either corpus, query or method are missing from query params.
        """
        su = UserFactory(is_superuser=True)
        url = reverse('search')

        self.client.force_authenticate(user=su)
        response = self.client.get(url + '?query=document&method=elastic', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_no_annotation_document_duplicates(self):
        """
        Ensure that a document already assigned to an annotation is not returned if a project 
        using annotation_document_duplicates=False is passed.
        """
        su = UserFactory(is_superuser=True)
        doc = DocumentFactory(content='a new document')
        project = ProjectFactory(corpora=[doc.corpus], annotation_document_duplicates=False)
        task = TaskFactory(project=project)
        AnnotationFactory(task=task, documents=[doc])
        url = reverse('search')
        query = '?query=document&corpus={}&method=elastic&project={}'.format(doc.corpus.id, project.id)

        self.client.force_authenticate(user=su)
        response = self.client.get(url + query, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class TestSearchMethodsView(APITestCase):
    def test_view_methods(self):
        """
        Ensure that the available search methods are returned.
        """
        user = UserFactory()
        url = reverse('search_methods')

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0], 'elastic')
        self.assertEqual(response.data[1], 'sentence_embedding')

    def test_deny_not_authenticated(self):
        """
        Ensure the search methods can only be viewed by authenticated users.
        """
        url = reverse('search_methods')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
