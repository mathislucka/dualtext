from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Task, Corpus, Document, Annotation, Label
from .helpers import run_standard_setup

class TestAnnotationListView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']
        task = Task(name='Task 1', annotator=self.user, project=self.project)
        task.save()
        self.task = task

        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('annotation_list', args=[self.task.id])
    
    def test_creation(self):
        """
        Ensure a new annotation can be created by a superuser.
        """
        data = {'documents': [self.document.id], 'corpus': [self.corpus.id]}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Annotation.objects.count(), 1)
        self.assertEqual(Annotation.objects.get(id=1).documents.all()[0], self.document)
        self.assertEqual(Annotation.objects.get(id=1).task, self.task)

    def test_superuser_view(self):
        """
        Ensure a superuser can view all annotations.
        """
        a1 = Annotation(task=self.task)
        a1.save()
        a1.documents.add(self.document)
        a1.save()

        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['documents'], [self.document.id])
        self.assertEqual(response.data[0]['task'], self.task.id)

    def test_view_only_allowed(self):
        """
        Ensure users can only view annotations that are children of tasks where the user is assigned as annotator.
        """
        t2 = Task(annotator=self.user, project=self.project, name='Assigned Task')
        t2.save()
        t3 = Task(annotator=self.superuser, project=self.project, name='Not assigned task')
        t3.save()
        
        a1 = Annotation(task=self.task)
        a1.save()
        a1.documents.add(self.document)
        a1.save()

        a2 = Annotation(task=t2)
        a2.save()
        a2.documents.add(self.document)
        a2.save()

        a3 = Annotation(task=t3)
        a3.save()
        a3.documents.add(self.document)
        a3.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        response_2 = self.client.get(reverse('annotation_list', args=[t2.id]))
        response_3 = self.client.get(reverse('annotation_list', args=[t3.id]))

        response_2_task = Task.objects.get(id=response_2.data[0]['task'])
        response_task = Task.objects.get(id=response.data[0]['task'])
        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response_task.annotator, self.user)
        
        self.assertEqual(len(response_2.data), 1)
        self.assertEqual(response_2_task.annotator, self.user)

        self.assertEqual(len(response_3.data), 0)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create annotations.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see annotations.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestAnnotationDetailView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']
        
        task = Task(name='Task 1', annotator=self.user, project=self.project)
        task.save()
        self.task = task
        
        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        annotation = Annotation(task=self.task)
        annotation.save()
        annotation.documents.add(self.document)
        annotation.save()
        self.annotation = annotation

        self.url = reverse('annotation_detail', args=[self.annotation.id])
    
    def test_annotator_view(self):
        """
        Ensure that annotators of a task can view an annotation.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        response_task_id = response.data['task']
        
        self.assertEqual(response_task_id, self.task.id)
        self.assertEqual(Task.objects.get(id=response_task_id).annotator, self.user)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all annotations.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.annotation.id)
        self.assertEqual(response.data['task'], self.task.id)
    
    def test_annotator_edit(self):
        """
        Ensure that annotators can edit an annotation.
        """
        label = Label(name="annotator", project=self.project, color={'standard': '#97C0E8', 'light': '#EAF2FA'})
        label.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {'labels': [label.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Annotation.objects.get(id=response.data['id']).labels.all()[0], label)

    def test_superuser_edit(self):
        """
        Ensure that superusers can edit an annotation.
        """
        label = Label(name="annotator", project=self.project, color={'standard': '#97C0E8', 'light': '#EAF2FA'})
        label.save()

        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(self.url, {'labels': [label.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Annotation.objects.get(id=response.data['id']).labels.all()[0], label)

    def test_deny_non_annotator_view(self):
        """
        Ensure that users who are neither annotator nor reviewer can't see an annotation.
        """
        self.task.annotator = self.superuser
        self.task.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_non_annotator_edit(self):
        """
        Ensure that users who are neither annotator nor reviewer can't edit an annotation.
        """
        self.task.annotator = self.superuser
        self.task.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)