from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Label, Project
from .helpers import run_standard_setup

class TestLabelListView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.project = standards['project']
        self.group = standards['group']
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.url = reverse('label_list', args=[self.project.id])
        self.data = {'name': 'TestLabel'}
    
    def test_creation(self):
        """
        Ensure a new label can be created by a superuser
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, self.data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(Label.objects.get(id=1).name, 'TestLabel')
        self.assertEqual(Label.objects.get().project, self.project)
    
    def test_unique_name(self):
        """
        Ensure that label names are unique within a project.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, self.data, format='json')
        response_2 = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Label.objects.count(), 1)
    
    def test_automatic_color_allocation(self):
        """
        Ensure a new label automatically gets a color on creation.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.get(id=1).color, {'standard': '#97E8D8', 'light': '#EAFAF7'})
    
    def test_superuser_view(self):
        """
        Ensure superusers can always view labels.
        """
        label = Label(name='TestLabel', project=self.project, color={'standard': '#97C0E8', 'light': '#EAF2FA'})
        label.save()
        self.client.force_authenticate(user=self.superuser)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data[0]['name'], label.name)
        self.assertEqual(response.data[0]['project'], label.project.id)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create labels
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        """
        Ensure a list of all labels can be viewed by project members
        """
        label = Label(name='TestLabel', project=self.project, color={'standard': '#97C0E8', 'light': '#EAF2FA'})
        label.save()
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data[0]['name'], label.name)
        self.assertEqual(response.data[0]['project'], label.project.id)

    def test_list_project_only(self):
        """
        Ensure only labels from a single project are listed.
        """
        p2 = Project(name="Second", creator=self.superuser)
        p2.save()
        p2.allowed_groups.add(self.group)
        p2.save()
        l1 = Label(name="TestLabel", project=self.project, color={'standard': '#97C0E8', 'light': '#EAF2FA'})
        l1.save()
        l2 = Label(name="Second", project=p2, color={'standard': '#97C0E8', 'light': '#EAF2FA'})
        l2.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], l1.name)

    def test_deny_list_not_project_member(self):
        """
        Ensure only project members can view the list.
        """
        user = User(username='notAllowed')
        user.save()

        self.client.force_authenticate(user=user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)