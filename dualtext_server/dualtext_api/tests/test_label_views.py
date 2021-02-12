from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Label
from .factories import UserFactory, GroupFactory, CorpusFactory, ProjectFactory, DocumentFactory, LabelFactory

class TestLabelListView(APITestCase):    
    def test_creation(self):
        """
        Ensure a new label can be created by a superuser
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('label_list', args=[project.id])
        data = {'name': 'TestLabel', 'key_code': 'a'}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(Label.objects.get(id=1).name, 'TestLabel')
        self.assertEqual(Label.objects.get().project, project)

    def test_unique_name(self):
        """
        Ensure that label names are unique within a project.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('label_list', args=[project.id])
        data = {'name': 'TestLabel', 'key_code': 'a'}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')
        response_2 = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Label.objects.count(), 1)

    def test_unique_key_code(self):
        """
        Ensure that key codes are unique within a project.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('label_list', args=[project.id])
        label_1 = {'name': 'TestLabel', 'key_code': 'a'}
        label_2 = {'name': 'TestLabel 2', 'key_code': 'a'}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, label_1, format='json')
        response_2 = self.client.post(url, label_2, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_key_code_a_to_z(self):
        """
        Ensure that key codes are outside of the a-zA-Z range are rejected.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('label_list', args=[project.id])
        data = {'name': 'TestLabel', 'key_code': 2}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_automatic_color_allocation(self):
        """
        Ensure a new label automatically gets a color on creation.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('label_list', args=[project.id])
        data = {'name': 'TestLabel', 'key_code': 'a'}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.get(id=1).color, {'standard': '#97E8D8', 'light': '#EAFAF7'})

    def test_superuser_view(self):
        """
        Ensure superusers can always view labels.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('label_list', args=[project.id])
        label = LabelFactory(project=project)

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data[0]['name'], label.name)
        self.assertEqual(response.data[0]['project'], label.project.id)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create labels
        """
        user = UserFactory()
        project = ProjectFactory()
        url = reverse('label_list', args=[project.id])
        data = {'name': 'TestLabel', 'key_code': 'a'}

        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        """
        Ensure a list of all labels can be viewed by project members
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        label = LabelFactory(project=project)
        url = reverse('label_list', args=[project.id])
        
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data[0]['name'], label.name)
        self.assertEqual(response.data[0]['project'], label.project.id)

    def test_list_project_only(self):
        """
        Ensure only labels from a single project are listed.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        label = LabelFactory(project=project)
        project_2 = ProjectFactory(allowed_groups=[group])
        LabelFactory(project=project_2)
        url = reverse('label_list', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], label.name)

    def test_deny_list_not_project_member(self):
        """
        Ensure only project members can view the list.
        """
        user = UserFactory()
        label = LabelFactory()
        url = reverse('label_list', args=[label.project.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
