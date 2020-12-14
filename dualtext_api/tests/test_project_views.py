from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Project
from .helpers import run_standard_setup

class TestProjectListView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']
        self.url = reverse('project_list')

    def test_creation(self):
        """
        Ensure a new project can be created by a superuser.
        """
        data = {'name': 'Test Project'}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Project.objects.get(id=2).name, 'Test Project')
        self.assertEqual(Project.objects.get(id=2).creator, self.superuser)

    def test_superuser_view(self):
        """
        Ensure a superuser can view all projects.
        """
        p2 = Project(name='Foo', creator=self.user)
        p2.save()
        p3 = Project(name='Bar', creator=self.user)
        p3.save()

        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[1]['name'], p2.name)
        self.assertEqual(response.data[2]['name'], p3.name)

    def test_view_only_allowed(self):
        """
        Ensure users can only view projects that they are allowed to see.
        """
        p2 = Project(name='Foo', creator=self.superuser)
        p2.save()
        p3 = Project(name='Bar', creator=self.superuser)
        p3.save()
        p3.allowed_groups.add(self.group)
        p3.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.project.name)
        self.assertEqual(response.data[1]['name'], p3.name)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create projects.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)