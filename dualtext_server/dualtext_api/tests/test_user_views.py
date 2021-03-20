from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Task, Annotation
from .factories import UserFactory, GroupFactory, ProjectFactory, TaskFactory, AnnotationFactory

class TestCurrentUserView(APITestCase):
    def test_current_user(self):
        """
        Ensure the current user is returned.
        """
        user = UserFactory()
        url = reverse('current_user')

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], user.id)

class TestCurrentUserStatisticsView(APITestCase):
    def test_current_user_statistics(self):
        """
        Ensure that the correct stats for a user are returned.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        task_1 = TaskFactory(project=project, annotator=user, is_finished=True, name='1')
        task_2 = TaskFactory(project=project, annotator=user, is_finished=True, name='2')
        task_3 = TaskFactory(project=project, annotator=user, action=Task.REVIEW, copied_from=task_1, name='3')
        task_4 = TaskFactory(project=project, annotator=user, action=Task.REVIEW, copied_from=task_1, is_finished=True, name='4')
        anno_1 = AnnotationFactory(task=task_1)
        anno_2 = AnnotationFactory(task=task_2)
        anno_3 = AnnotationFactory(task=task_2)
        AnnotationFactory(task=task_2)
        AnnotationFactory(task=task_3, action=Annotation.REVIEW, copied_from=anno_1)
        AnnotationFactory(task=task_4, action=Annotation.REVIEW, copied_from=anno_2)
        AnnotationFactory(task=task_4, action=Annotation.REVIEW, copied_from=anno_3)
        url = reverse('current_user_statistics')

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tasks']['total'], 4)
        self.assertEqual(response.data['tasks']['annotations']['open'], 0)
        self.assertEqual(response.data['tasks']['annotations']['closed'], 2)
        self.assertEqual(response.data['tasks']['reviews']['open'], 1)
        self.assertEqual(response.data['tasks']['reviews']['closed'], 1)
        self.assertEqual(response.data['annotations']['annotator']['total'], 4)
        self.assertEqual(response.data['annotations']['annotator']['open'], 0)
        self.assertEqual(response.data['annotations']['annotator']['closed'], 4)
        self.assertEqual(response.data['annotations']['reviewer']['total'], 3)
        self.assertEqual(response.data['annotations']['reviewer']['open'], 1)
        self.assertEqual(response.data['annotations']['reviewer']['closed'], 2)