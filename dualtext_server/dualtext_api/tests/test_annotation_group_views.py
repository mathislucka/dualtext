from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import AnnotationGroup
from .factories import UserFactory, GroupFactory, TaskFactory, AnnotationGroupFactory, ProjectFactory

class TestAnnotationGroupListView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure that users can view annotation groups when they are assigned as the group's task annotators.
        """
        user = UserFactory()
        task = TaskFactory(annotator=user)
        annotation_group = AnnotationGroupFactory(task=task)
        url = reverse('annotation_group_list', args=[task.id])

        # create a second annotation group belonging to a different task
        AnnotationGroupFactory()


        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['task'], task.id)

    def test_deny_non_annotator_view(self):
        """
        Ensure that users can't see annotation groups when they are not assigned as annotators of the group's task.
        """
        user = UserFactory()
        task = TaskFactory()
        annotation_group = AnnotationGroupFactory(task=task)
        url = reverse('annotation_group_list', args=[task.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 0)

    def test_superuser_view(self):
        """
        Ensure that superusers can view all annotation groups belonging to a specific task.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        annotation_group = AnnotationGroupFactory(task=task)
        url = reverse('annotation_group_list', args=[task.id])

        # create a second annotation group belonging to a different task
        p1 = ProjectFactory(name='different')
        task_2 = TaskFactory(project=p1)
        AnnotationGroupFactory(task=task_2)


        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['task'], task.id)

    def test_superuser_create(self):
        """
        Ensure that superusers can create an annotation group.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        data = {'task': task.id}
        url = reverse('annotation_group_list', args=[task.id])

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')

        created_annotation_group = AnnotationGroup.objects.get(id=response.data['id'])
        self.assertEqual(created_annotation_group.task.id, task.id)

    def test_deny_non_superuser_create(self):
        """
        Ensure that normal users can't create an annotation group.
        """
        user = UserFactory()
        task = TaskFactory()
        url = reverse('annotation_group_list', args=[task.id])

        self.client.force_authenticate(user=user)
        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestAnnotationGroupDetailView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure that users can view a single annotation group if they are the annotator of the group's task.
        """
        user = UserFactory()
        task = TaskFactory(annotator=user)
        AnnotationGroupFactory(task=task)
        url = reverse('annotation_group_detail', args=[task.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data['task'], task.id)

    def test_superuser_view(self):
        """
        Ensure that superusers can view all annotation groups.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        AnnotationGroupFactory(task=task)
        url = reverse('annotation_group_detail', args=[task.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data['task'], task.id)

    def test_deny_non_annotator_view(self):
        """
        Ensure an annotation group can't be viewed by a user who is not the annotator of the group's task.
        """
        user = UserFactory()
        task = TaskFactory()
        AnnotationGroupFactory(task=task)
        url = reverse('annotation_group_detail', args=[task.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

