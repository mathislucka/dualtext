from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Project, Label, Annotation, Document, Task
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

    def test_unique_name(self):
        """
        Ensure that project names are unique.
        """
        data = {'name': 'Test Project'}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        response_2 = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see projects.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestProjectDetailView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']
        self.url = reverse('project_detail', args=[self.project.id])

    def test_allowed_view(self):
        """
        Ensure projects can be viewed by project members.
        """
        self.client.force_authenticate(user=self.user)
        self.project.allowed_groups.add(self.group)
        self.project.save()

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.project.id)
    
    def test_deny_access_non_members(self):
        """
        Ensure users who are not project members can't view a project.
        """
        self.client.force_authenticate(user=self.user)
        self.project.allowed_groups.remove(self.group)
        self.project.save()

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_superuser_view(self):
        """
        Ensure a project can be viewed by a superuser.
        """
        self.client.force_authenticate(user=self.superuser)
        self.project.allowed_groups.remove(self.group)
        self.project.save()

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.project.id)

    def test_superuser_edit(self):
        """
        Ensure a superuser can update a project.
        """
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'A new name'}

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'A new name')

    def test_deny_non_superuser_edit(self):
        """
        Ensure only superusers can update a project.
        """
        self.client.force_authenticate(user=self.user)
        data = {'name': 'A new name'}

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_delete(self):
        """
        Ensure that superusers can delete a project.
        """
        t = Task(project=self.project, name="task to delete")
        t.save()

        a = Annotation(task=t)
        a.save()

        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.url, format='json')
        try:
            project = Project.objects.get(id=self.project.id)
        except Project.DoesNotExist:
            project = None

        try:
            task = Task.objects.get(id=t.id)
        except Task.DoesNotExist:
            task = None

        try:
            annotation = Annotation.objects.get(id=a.id)
        except Annotation.DoesNotExist:
            annotation = None

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(project, None)
        self.assertEqual(task, None)
        self.assertEqual(annotation, None)

    def test_deny_non_superuser_delete(self):
        """
        Ensure that users who are not superusers can't delete a project.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestProjectStatisticsView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']
        self.url = reverse('project_statistics', args=[self.project.id])

    def test_allowed_view(self):
        """
        Ensure project statistics can be viewed by project members.
        """
        self.client.force_authenticate(user=self.user)
        self.project.allowed_groups.add(self.group)
        self.project.save()

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_deny_access_non_members(self):
        """
        Ensure users who are not project members can't view project statistics
        """
        self.client.force_authenticate(user=self.user)
        p2 = Project(name='Foo', creator=self.superuser)
        p2.save()
        url = reverse('project_statistics', args=[p2.id])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_label_distribution(self):
        """
        Ensure the response contains the current distribution of labels inside the project.
        """
        l1 = Label(name='foo', project=self.project, color={"standard": "color"})
        l1.save()
        l2 = Label(name='bar', project=self.project, color={"standard": "color"})
        l2.save()
        l3 = Label(name='foobar', project=self.project, color={"standard": "color"})
        l3.save()

        t1 = Task(name='t1', project=self.project, annotator=self.user)
        t1.save()
        t2 = Task(name='t2', project=self.project, annotator=self.user)
        t2.save()

        a1 = Annotation(task=t1)
        a1.save()
        a1.labels.add(l1)
        a1.labels.add(l2)
        a1.save()

        a2 = Annotation(task=t2)
        a2.save()
        a2.labels.add(l1)
        a2.labels.add(l3)
        a2.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.data['labels']['absolute']['foo'], 2)
        self.assertEqual(response.data['labels']['relative']['bar'], 0.25)
        self.assertEqual(response.data['labels']['total'], 4)

    def test_reviewer_labels_override_annotator(self):
        """
        Ensure that reviewer labels are counted if there is a review task.
        """
        l1 = Label(name='foo', project=self.project, color={"standard": "color"})
        l1.save()
        l2 = Label(name='bar', project=self.project, color={"standard": "color"})
        l2.save()
        l3 = Label(name='foobar', project=self.project, color={"standard": "color"})
        l3.save()

        t1 = Task(name='t1', project=self.project, annotator=self.user)
        t1.save()
        t2 = Task(name='t2', project=self.project, annotator=self.user, action=Task.REVIEW, copied_from=t1)
        t2.save()

        a1 = Annotation(task=t1)
        a1.save()
        a1.labels.add(l1)
        a1.labels.add(l3)
        a1.labels.add(l2)
        a1.save()

        a2 = Annotation(task=t2, copied_from=a1, action=Annotation.REVIEW)
        a2.save()
        a2.labels.add(l2)
        a2.labels.add(l3)
        a2.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.data['labels']['absolute']['foobar'], 1)
        self.assertEqual(response.data['labels']['relative']['foo'], 0)
        self.assertEqual(response.data['labels']['total'], 2)

    def test_task_counts(self):
        """
        Ensure that statistics contain the total count of tasks as well as absolute and percentage values for
        annotated and reviewed tasks.
        """
        t1 = Task(name='t1', project=self.project, annotator=self.user, is_finished=True)
        t1.save()
        t2 = Task(name='t2', project=self.project, annotator=self.user, action=Task.REVIEW, is_finished=True, copied_from=t1)
        t2.save()
        t3 = Task(name='t3', project=self.project, annotator=self.user)
        t3.save()
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.data['tasks']['total'], 3)
        self.assertEqual(response.data['tasks']['annotated_absolute'], 1)
        self.assertEqual(response.data['tasks']['annotated_relative'], 0.33)
        self.assertEqual(response.data['tasks']['reviewed_absolute'], 1)
        self.assertEqual(response.data['tasks']['reviewed_relative'], 0.33)
    
    def test_annotation_counts(self):
        """
        Ensure that statistics contain the total count of annotations as well as absolute and percentage values for
        annotated and reviewed annotations.
        """
        t1 = Task(name='t1', project=self.project, annotator=self.user, is_finished=True)
        t1.save()
        t2 = Task(name='t2', project=self.project, annotator=self.user, action=Task.REVIEW, is_finished=True, copied_from=t1)
        t2.save()
        t3 = Task(name='t3', project=self.project, annotator=self.user)
        t3.save()

        a1 = Annotation(task=t1)
        a1.save()
        a2 = Annotation(task=t2, action=Annotation.REVIEW, copied_from=a1)
        a2.save()
        a3 = Annotation(task=t2, action=Annotation.REVIEW, copied_from=a1)
        a3.save()
        a4 = Annotation(task=t2, action=Annotation.REVIEW, copied_from=a1)
        a4.save()
        a5 = Annotation(task=t3)
        a5.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.data['annotations']['total'], 5)
        self.assertEqual(response.data['annotations']['annotated_absolute'], 1)
        self.assertEqual(response.data['annotations']['annotated_relative'], 0.2)
        self.assertEqual(response.data['annotations']['reviewed_absolute'], 3)
        self.assertEqual(response.data['annotations']['reviewed_relative'], 0.6)

