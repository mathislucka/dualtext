from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Project, Task, Annotation
from .helpers import run_standard_setup

class TestCurrentUserView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.project = standards['project']
        self.group = standards['group']
        self.user = standards['user']
        self.superuser = standards['superuser']

    def test_current_user(self):
        """
        Ensure the current user is returned.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('current_user'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.superuser.id)

class TestCurrentUserStatisticsView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.project = standards['project']
        self.group = standards['group']
        self.user = standards['user']
        self.superuser = standards['superuser']

    def test_current_user_statistics(self):
        """
        Ensure that the correct stats for a user are returned.
        """
        t1 = Task(name='t1', project=self.project, annotator=self.user, reviewer=self.superuser, is_annotated=True)
        t1.save()
        t2 = Task(name='t2', project=self.project, annotator=self.user, reviewer=self.superuser, is_reviewed=True)
        t2.save()
        t3 = Task(name='t3', project=self.project, annotator=self.user, reviewer=self.superuser)
        t3.save()
        t4 = Task(name='t4', project=self.project, annotator=self.superuser, reviewer=self.user)
        t4.save()
        t5 = Task(name='t5', project=self.project, annotator=self.superuser, reviewer=self.user, is_annotated=True)
        t5.save()
        t6 = Task(name='t6', project=self.project, annotator=self.superuser, reviewer=self.user, is_reviewed=True)
        t6.save()
        t7 = Task(name='t6', project=self.project, annotator=self.superuser, reviewer=self.superuser, is_reviewed=True)
        t7.save()

        a1 = Annotation(task=t1)
        a1.save()
        a2 = Annotation(task=t2)
        a2.save()
        a3 = Annotation(task=t2)
        a3.save()
        a4 = Annotation(task=t2)
        a4.save()
        a5 = Annotation(task=t3)
        a5.save()
        a6 = Annotation(task=t4)
        a6.save()
        a7 = Annotation(task=t4)
        a7.save()
        a8 = Annotation(task=t5)
        a8.save()
        a9 = Annotation(task=t6)
        a9.save()
        a10 = Annotation(task=t6)
        a10.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('current_user_statistics'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tasks']['total'], 6)
        self.assertEqual(response.data['tasks']['annotations']['open'], 2)
        self.assertEqual(response.data['tasks']['annotations']['closed'], 1)
        self.assertEqual(response.data['tasks']['reviews']['open'], 2)
        self.assertEqual(response.data['tasks']['reviews']['closed'], 1)
        self.assertEqual(response.data['annotations']['annotator']['total'], 5)
        self.assertEqual(response.data['annotations']['annotator']['open'], 4)
        self.assertEqual(response.data['annotations']['annotator']['closed'], 1)
        self.assertEqual(response.data['annotations']['reviewer']['total'], 5)
        self.assertEqual(response.data['annotations']['reviewer']['open'], 3)
        self.assertEqual(response.data['annotations']['reviewer']['closed'], 2)