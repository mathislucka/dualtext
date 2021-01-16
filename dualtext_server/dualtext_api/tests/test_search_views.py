from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Corpus, Document, Annotation, Project, Task
from .helpers import run_standard_setup

class TestSearchView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']

        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        corpus.allowed_groups.add(self.group)
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('search')
    
    def test_elasticsearch_results(self):
        """
        Ensure the search with elasticsearch will return all matching documents in a corpus.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url + '?query=document&corpus=1&method=elastic', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['content'], self.document.content)

    def test_deny_not_authenticated(self):
        """
        Ensure the search can only be used by authenticated users.
        """
        response = self.client.get(self.url + '?query=document&corpus=1&method=elastic', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deny_non_member(self):
        """
        Ensure that a user only gets results from a corpus if they are in the allowed_groups.
        """
        self.corpus.allowed_groups.remove(self.group)
        self.corpus.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url + '?query=document&corpus=1&method=elastic', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_no_results_incomplete_params(self):
        """
        Ensure that no results are returned if either corpus, query or method are missing from query params.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url + '?query=document&method=elastic', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_no_annotation_document_duplicates(self):
        """
        Ensure that a document already assigned to an annotation is not returned if a project using annotation_document_duplicates=False is passed.
        """
        p = Project(name="a project", annotation_document_duplicates=False)
        p.save()
        p.corpora.add(self.corpus)
        p.save()
        t = Task(project=p, name='A Task')
        t.save()
        
        a = Annotation(task=t)
        a.save()
        a.documents.add(self.document)
        a.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url + '?query=document&corpus=1&method=elastic&project={}'.format(p.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        def test_superuser_elasticsearch_results(self):
        """
        Ensure that superusers have access to all corpora through search.
        """
        self.client.force_authenticate(user=self.superuser)
        self.corpus.allowed_groups.remove(self.group)
        self.corpus.save()
        response = self.client.get(self.url + '?query=document&corpus=1&method=elastic', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['content'], self.document.content)
