from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Annotation, Run, Lap
from .factories import AnnotationFactory, DocumentFactory, TaskFactory, UserFactory, LabelFactory, AnnotationGroupFactory
from .factories import ProjectFactory
from django.utils import timezone
import time

class TestAnnotationListView(APITestCase):
    def test_creation(self):
        """
        Ensure a new annotation can be created by a superuser.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        doc = DocumentFactory()
        data = {'documents': [doc.id]}
        url = reverse('annotation_list', args=[task.id])
        
        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Annotation.objects.count(), 1)
        self.assertEqual(Annotation.objects.get(id=1).documents.all()[0], doc)
        self.assertEqual(Annotation.objects.get(id=1).task, task)

    def test_same_task_group(self):
        """
        Ensure an annotation can't have a group with a different task.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        group = AnnotationGroupFactory()
        data = {'annotation_group': group.id}
        url = reverse('annotation_list', args=[task.id])
        
        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_timetracking_on_creation(self):
        """
        Ensure that no timetracking runs or laps are created when creating an annotation
        with documents or labels
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        doc = DocumentFactory()
        label = LabelFactory(project=task.project)
        data = {'documents': [doc.id], 'labels': [label.id]}
        url = reverse('annotation_list', args=[task.id])
        
        self.client.force_authenticate(user=su)
        self.client.post(url, data, format='json')

        runs = Run.objects.all()
        laps = Lap.objects.all()

        self.assertEqual(len(runs), 0)
        self.assertEqual(len(laps), 0)

    def test_no_exceeding_max_documents(self):
        """
        Ensure that an annotation can't have more documents than the project's maximum number of documents.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory(max_documents=5)
        task = TaskFactory()
        docs = DocumentFactory.create_batch(6)
        docs = [doc.id for doc in docs]
        data = {'documents': docs}
        url = reverse('annotation_list', args=[task.id])
        
        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_view(self):
        """
        Ensure a superuser can view all annotations.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        doc = DocumentFactory()
        anno = AnnotationFactory(documents=[doc], task=task)
        url = reverse('annotation_list', args=[task.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['documents'], [doc.id])
        self.assertEqual(response.data[0]['id'], anno.id)

    def test_label_id_filter(self):
        """
        Ensure annotations can be filtered by label id.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        label = LabelFactory(project=task.project)
        anno = AnnotationFactory(labels=[label], task=task)
        AnnotationFactory(task=task)
        url = reverse('annotation_list', args=[task.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url + f'?label={label.id}', format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['labels'], [label.id])
        self.assertEqual(response.data[0]['id'], anno.id)

    def test_label_name_filter(self):
        """
        Ensure annotations can be filtered by label name.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        label = LabelFactory(project=task.project)
        anno = AnnotationFactory(labels=[label], task=task)
        AnnotationFactory(task=task)
        url = reverse('annotation_list', args=[task.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url + f'?label_name={label.name}', format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['labels'], [label.id])
        self.assertEqual(response.data[0]['id'], anno.id)

    def test_view_only_allowed(self):
        """
        Ensure users can only view annotations that are children of tasks where the user is assigned as annotator.
        """
        user = UserFactory()
        su = UserFactory(is_superuser=True)
        task_1 = TaskFactory(annotator=user)
        task_2 = TaskFactory(annotator=su)
        anno_1 = AnnotationFactory(task=task_1)
        AnnotationFactory(task=task_2)
        url_1 = reverse('annotation_list', args=[task_1.id])
        url_2 = reverse('annotation_list', args=[task_2.id])

        self.client.force_authenticate(user=user)
        response_1 = self.client.get(url_1, format='json')
        response_2 = self.client.get(url_2, format='json')

        self.assertEqual(len(response_1.data), 1)
        self.assertEqual(response_1.data[0]['id'], anno_1.id)
        self.assertEqual(len(response_2.data), 0)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create annotations.
        """
        user = UserFactory()
        task = TaskFactory()
        url = reverse('annotation_list', args=[task.id])

        self.client.force_authenticate(user=user)
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see annotations.
        """
        task = TaskFactory()
        url = reverse('annotation_list', args=[task.id])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestAnnotationDetailView(APITestCase):
    def test_annotator_view(self):
        """
        Ensure that annotators of a task can view an annotation.
        """
        user = UserFactory()
        task = TaskFactory(annotator=user)
        anno = AnnotationFactory(task=task)
        url = reverse('annotation_detail', args=[anno.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], anno.id)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all annotations.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        anno = AnnotationFactory(task=task)
        url = reverse('annotation_detail', args=[anno.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], anno.id)

    def test_annotator_edit(self):
        """
        Ensure that annotators can edit an annotation.
        """
        user = UserFactory()
        task = TaskFactory(annotator=user)
        lab = LabelFactory()
        annotation = AnnotationFactory(task=task, labels=[lab])
        label = LabelFactory()
        url = reverse('annotation_detail', args=[annotation.id])

        self.client.force_authenticate(user=user)
        response = self.client.patch(url, {'labels': [label.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Annotation.objects.get(id=response.data['id']).labels.all()[0], label)

    def test_superuser_edit(self):
        """
        Ensure that superusers can edit an annotation.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory(annotator=su)
        annotation = AnnotationFactory(task=task)
        label = LabelFactory()
        url = reverse('annotation_detail', args=[annotation.id])

        self.client.force_authenticate(user=su)
        response = self.client.patch(url, {'labels': [label.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Annotation.objects.get(id=response.data['id']).labels.all()[0], label)

    def test_deny_non_annotator_view(self):
        """
        Ensure that users who are neither annotator nor a superuser can't see an annotation.
        """
        user = UserFactory()
        anno = AnnotationFactory()
        url = reverse('annotation_detail', args=[anno.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_non_annotator_edit(self):
        """
        Ensure that users who are neither annotator nor a superuser can't edit an annotation.
        """
        user = UserFactory()
        anno = AnnotationFactory()
        url = reverse('annotation_detail', args=[anno.id])

        self.client.force_authenticate(user=user)
        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_timetracking_on_update(self):
        """
        Ensure that a timetracking Lap and possibly a timetracking run is created when the
        label or documents of an annotation get an update.
        """
        su = UserFactory(is_superuser=True)
        anno = AnnotationFactory()
        label = LabelFactory()
        url = reverse('annotation_detail', args=[anno.id])
        
        self.client.force_authenticate(user=su)
        self.client.patch(url, {'labels': [label.id]}, format='json')

        run = Run.objects.all()
        lap = Lap.objects.all()
        self.assertEqual(len(run), 1)
        self.assertEqual(len(lap), 1)

    def test_new_run_when_idle(self):
        """
        Ensure that a timetracking Lap is assigned to a newly created Run if the last Run
        was idle for more than 300 seconds.
        """
        su = UserFactory(is_superuser=True)
        anno = AnnotationFactory()
        label = LabelFactory()
        url = reverse('annotation_detail', args=[anno.id])

        self.client.force_authenticate(user=su)
        self.client.patch(url, {'labels': [label.id]}, format='json')

        now = timezone.now()
        idle = now - timezone.timedelta(seconds=301)
        run = Run.objects.all().first()
        run.lap_set.filter(id=1).update(created_at=idle, run_id=run.id, annotation_id=anno.id)

        self.client.patch(url, {'labels': []}, format='json')
        run = Run.objects.all()
        lap = Lap.objects.all()

        self.assertEqual(len(run), 2)
        self.assertEqual(len(lap), 2)
