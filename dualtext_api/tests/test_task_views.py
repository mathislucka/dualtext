from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Project, Task
from .helpers import run_standard_setup

class TestTaskListView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.project = standards['project']
        self.group = standards['group']
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.url = reverse('task_list', args=[self.project.id])
    
    def test_creation(self):
        """
        Ensure a new task can be created by a superuser.
        """
        data = {'name': 'Test Task', 'annotator': self.user.id, 'reviewer': self.superuser.id}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get(id=1).name, 'Test Task')
        self.assertEqual(Task.objects.get().project, self.project)

    def test_superuser_view(self):
        """
        Ensure a superuser can view all tasks.
        """
        t1 = Task(name="new task", project=self.project, annotator=self.user)
        t1.save()
        t2 = Task(name='second task', project=self.project, annotator=self.user)
        t2.save()

        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], t1.name)
        self.assertEqual(response.data[1]['name'], t2.name)

    def test_list(self):
        """
        A user should see all tasks assigned to them as annotator or reviewer
        """
        t1 = Task(name="new task", project=self.project, annotator=self.user)
        t1.save()
        t2 = Task(name='second task', project=self.project, reviewer=self.user)
        t2.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], t1.name)
        self.assertEqual(response.data[1]['name'], t2.name)

    def test_list_project_only(self):
        """
        A user should only see tasks within the specified project.
        """
        p2 = Project(name="lala", creator=self.superuser)
        p2.save()
        t1 = Task(name="new task", project=self.project, annotator=self.user)
        t1.save()
        t2 = Task(name='second task', project=p2, reviewer=self.user)
        t2.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], t1.name)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create tasks.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_only_assigned(self):
        """
        Users should only see tasks assigned to themselves.
        """
        t1 = Task(name="new task", project=self.project, annotator=self.superuser)
        t1.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 0)