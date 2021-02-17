from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Task
from .factories import UserFactory, TaskFactory, ProjectFactory, GroupFactory

class TestTaskListView(APITestCase):
    def test_creation(self):
        """
        Ensure a new task can be created by a superuser.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('task_list', args=[project.id])
        data = {'name': 'Test Task'}
        
        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')
        created_task = Task.objects.get(id=response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(created_task.name, 'Test Task')
        self.assertEqual(created_task.project, project)

    def test_unique_name_in_project(self):
        """
        Ensure that task names are unique within a project.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('task_list', args=[project.id])
        data = {'name': 'Test Task'}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')
        response_2 = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_view(self):
        """
        Ensure a superuser can view all tasks.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        task_1 = TaskFactory(project=project, name="task_1")
        task_2 = TaskFactory(project=project, name="task_2")
        url = reverse('task_list', args=[project.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], task_1.name)
        self.assertEqual(response.data[1]['name'], task_2.name)

    def test_list(self):
        """
        A user should see all tasks assigned to them as annotator.
        """
        user = UserFactory()
        project = ProjectFactory()
        task = TaskFactory(project=project, annotator=user)
        url = reverse('task_list', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], task.name)

    def test_list_project_only(self):
        """
        A user should only see tasks within the specified project.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        task = TaskFactory(project=project)
        TaskFactory()
        url = reverse('task_list', args=[project.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], task.name)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create tasks.
        """
        user = UserFactory()
        project = ProjectFactory()
        url = reverse('task_list', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_assigned(self):
        """
        Users should only see tasks assigned to themselves.
        """
        user = UserFactory()
        project = ProjectFactory()
        TaskFactory(project=project)
        url = reverse('task_list', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 0)

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see tasks.
        """
        project = ProjectFactory()
        url = reverse('task_list', args=[project.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestTaskDetailView(APITestCase):
    def test_annotator_task_view(self):
        """
        Ensure a task can be viewed by its annotator.
        """
        user = UserFactory()
        task = TaskFactory(annotator=user)
        url = reverse('task_detail', args=[task.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], task.name)

    def test_superuser_task_view(self):
        """
        Ensure that a task can always be viewed by a superuser.
        """
        su = UserFactory(is_superuser=True)
        task = TaskFactory()
        url = reverse('task_detail', args=[task.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], task.name)

    def test_deny_non_annotator_view(self):
        """
        Ensure a user can't view a task that they are not annotating.
        """
        user = UserFactory()
        task = TaskFactory()
        url = reverse('task_detail', args=[task.id])

        self.client.force_authenticate(user=user)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_autogenerate_review_task(self):
        """
        Ensure a review task is created when a task is marked as finished.
        """
        user = UserFactory()
        project = ProjectFactory(use_reviews=True)
        task = TaskFactory(annotator=user, project=project)
        url = reverse('task_detail', args=[task.id])

        self.client.force_authenticate(user=user)
        self.client.patch(url, { 'is_finished': True }, format='json')

        review_task = Task.objects.filter(copied_from=task).first()
        self.assertEqual(review_task.copied_from.id, task.id)
        self.assertEqual(review_task.action, 'review')


class TestClaimTaskView(APITestCase):
    def test_claimable_tasks(self):
        """
        Ensure that the number of unclaimed annotation tasks and unclaimed review tasks is returned.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        task = TaskFactory(project=project, annotator=None)
        TaskFactory(copied_from=task, project=project, action=Task.REVIEW, annotator=None)
        url = reverse('task_claimable', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['open_annotations'], 1)
        self.assertEqual(response.data['open_reviews'], 1)

    def test_annotation_task_claiming(self):
        """
        Ensure that the first task without an annotator is claimed.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        task = TaskFactory(project=project, annotator=None)
        url = reverse('task_claim', args=[project.id, 'annotation'])

        self.client.force_authenticate(user=user)
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], task.id)

    def test_review_task_claiming(self):
        """
        Ensure that the first annotated task without a reviewer is claimed.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        task = TaskFactory(project=project, annotator=None)
        review_task = TaskFactory(copied_from=task, project=project, action=Task.REVIEW, annotator=None)
        url = reverse('task_claim', args=[project.id, 'annotation'])
        
        url = reverse('task_claim', args=[project.id, 'review'])
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], review_task.id)

    def test_no_copied_from_claiming(self):
        """
        Ensure that a user won't claim a task that was copied from a task they annotated.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        task = TaskFactory(project=project, annotator=user)
        TaskFactory(copied_from=task, project=project, action=Task.REVIEW, annotator=None)
        url = reverse('task_claim', args=[project.id, 'review'])

        self.client.force_authenticate(user=user)
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_deny_non_members(self):
        """
        Ensure that only project members can claim a task.
        """
        user = UserFactory()
        project = ProjectFactory()
        task = TaskFactory(project=project)
        url = reverse('task_claim', args=[project.id, 'annotation'])

        self.client.force_authenticate(user=user)
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
