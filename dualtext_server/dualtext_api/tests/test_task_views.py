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
        data = {'name': 'Test Task', 'annotator': self.user.id}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get(id=1).name, 'Test Task')
        self.assertEqual(Task.objects.get().project, self.project)

    def test_unique_name_in_project(self):
        """
        Ensure that task names are unique within a project.
        """
        data = {'name': 'Test Task'}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        response_2 = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

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
        A user should see all tasks assigned to them as annotator.
        """
        t1 = Task(name="new task", project=self.project, annotator=self.user)
        t1.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], t1.name)

    def test_list_project_only(self):
        """
        A user should only see tasks within the specified project.
        """
        p2 = Project(name="lala", creator=self.superuser)
        p2.save()
        t1 = Task(name="new task", project=self.project, annotator=self.user)
        t1.save()
        t2 = Task(name='second task', project=p2, annotator=self.user)
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

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see tasks.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestTaskDetailView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.project = standards['project']
        self.group = standards['group']
        self.user = standards['user']
        self.superuser = standards['superuser']

    def test_annotator_task_view(self):
        """
        Ensure a task can be viewed by its annotator.
        """
        t = Task(name="task 1", annotator=self.user, project=self.project)
        t.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('task_detail', args=[t.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], t.name)

    def test_superuser_task_view(self):
        """
        Ensure that a task can always be viewed by a superuser.
        """
        t = Task(name="task 1", annotator=self.user, project=self.project)
        t.save()
        self.client.force_authenticate(user=self.superuser)
        url = reverse('task_detail', args=[t.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], t.name)

    def test_deny_non_annotator_view(self):
        """
        Ensure a user can't view a task that they are not annotating.
        """
        t = Task(name="task 1", project=self.project)
        t.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('task_detail', args=[t.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_autogenerate_review_task(self):
        """
        Ensure a review task is created when a task is marked as finished.
        """
        t = Task(name="task 1", annotator=self.user, project=self.project)
        t.save()
        self.project.use_reviews = True
        self.project.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('task_detail', args=[t.id])
        self.client.patch(url, { 'is_finished': True }, format='json')
        review_task = Task.objects.filter(copied_from=t).first()
        self.assertEqual(review_task.copied_from.id, t.id)
        self.assertEqual(review_task.action, 'review')


class TestClaimTaskView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.project = standards['project']
        self.group = standards['group']
        self.user = standards['user']
        self.superuser = standards['superuser']

    def test_claimable_tasks(self):
        """
        Ensure that the number of unclaimed annotation tasks and unclaimed review tasks is returned.
        """
        self.project.allowed_groups.add(self.group)
        self.project.save()
        self.user.groups.add(self.group)
        self.user.save()

        t1 = Task(name="first task", project=self.project)
        t1.save()
        t2 = Task(name="claimed task", project=self.project, action=Task.REVIEW, copied_from=t1)
        t2.save()

        url = reverse('task_claimable', args=[self.project.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['open_annotations'], 1)
        self.assertEqual(response.data['open_reviews'], 1)

    def test_annotation_task_claiming(self):
        """
        Ensure that the first task without an annotator is claimed.
        """
        self.project.allowed_groups.add(self.group)
        self.project.save()
        self.user.groups.add(self.group)
        self.user.save()

        t1 = Task(name="first task", project=self.project)
        t1.save()

        url = reverse('task_claim', args=[self.project.id, 'annotation'])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], t1.id)

    def test_review_task_claiming(self):
        """
        Ensure that the first annotated task without a reviewer is claimed.
        """
        self.project.allowed_groups.add(self.group)
        self.project.save()
        self.user.groups.add(self.group)
        self.user.save()

        t1 = Task(name="first task", project=self.project, action=Task.REVIEW)
        t1.save()

        url = reverse('task_claim', args=[self.project.id, 'review'])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], t1.id)

    def test_no_copied_from_claiming(self):
        """
        Ensure that a user won't claim a task that was copied from a task they annotated.
        """
        self.project.allowed_groups.add(self.group)
        self.project.save()
        self.user.groups.add(self.group)
        self.user.save()

        t = Task(name="original task", project=self.project, annotator=self.user)
        t.save()
        t1 = Task(name="first task", project=self.project, action=Task.REVIEW, copied_from=t)
        t1.save()

        url = reverse('task_claim', args=[self.project.id, 'review'])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_deny_non_members(self):
        """
        Ensure that only project members can claim a task.
        """
        self.project.allowed_groups.remove(self.group)
        self.project.save()
        t1 = Task(name="first task", project=self.project)
        t1.save()

        url = reverse('task_claim', args=[self.project.id, 'annotation'])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)