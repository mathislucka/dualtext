from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from dualtext_api.models import Project, Label, Annotation, Task, Run, Lap
from .factories import UserFactory, TaskFactory, ProjectFactory, AnnotationFactory, LabelFactory, GroupFactory
import datetime
import time

class TestProjectListView(APITestCase):
    def test_creation(self):
        """
        Ensure a new project can be created by a superuser.
        """
        su = UserFactory(is_superuser=True)
        url = reverse('project_list')
        data = {'name': 'Test Project'}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get(id=1).name, 'Test Project')
        self.assertEqual(Project.objects.get(id=1).creator, su)

    def test_unique_name(self):
        """
        Ensure that project names are unique.
        """
        su = UserFactory(is_superuser=True)
        url = reverse('project_list')
        data = {'name': 'Test Project'}

        self.client.force_authenticate(user=su)
        response = self.client.post(url, data, format='json')
        response_2 = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_view(self):
        """
        Ensure a superuser can view all projects.
        """
        su = UserFactory(is_superuser=True)
        projects = ProjectFactory.create_batch(size=5)
        url = reverse('project_list')

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]['name'], projects[0].name)
        self.assertEqual(response.data[4]['name'], projects[4].name)

    def test_view_only_allowed(self):
        """
        Ensure users can only view projects that they are allowed to see.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        ProjectFactory()
        url = reverse('project_list')

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], project.name)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create projects.
        """
        user = UserFactory()
        url = reverse('project_list')
        data = {'name': 'new project'}

        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_not_authenticated(self):
        """
        Ensure only authenticated users can see projects.
        """
        url = reverse('project_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestProjectDetailView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure projects can be viewed by project members.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        url = reverse('project_detail', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], project.id)
    
    def test_deny_access_non_members(self):
        """
        Ensure users who are not project members can't view a project.
        """
        user = UserFactory()
        project = ProjectFactory()
        url = reverse('project_detail', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_superuser_view(self):
        """
        Ensure a project can be viewed by a superuser.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('project_detail', args=[project.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], project.id)

    def test_superuser_edit(self):
        """
        Ensure a superuser can update a project.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        url = reverse('project_detail', args=[project.id])
        data = {'name': 'A new name'}

        self.client.force_authenticate(user=su)
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'A new name')

    def test_deny_non_superuser_edit(self):
        """
        Ensure only superusers can update a project.
        """
        user = UserFactory()
        project = ProjectFactory()
        url = reverse('project_detail', args=[project.id])
        data = {'name': 'A new name'}

        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_delete(self):
        """
        Ensure that superusers can delete a project (and that the deletion cascades).
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        task = TaskFactory(project=project)
        anno = AnnotationFactory(task=task)
        url = reverse('project_detail', args=[project.id])

        self.client.force_authenticate(user=su)
        response = self.client.delete(url, format='json')
    
        try:
            project = Project.objects.get(id=project.id)
        except Project.DoesNotExist:
            project = None

        try:
            task = Task.objects.get(id=task.id)
        except Task.DoesNotExist:
            task = None

        try:
            annotation = Annotation.objects.get(id=anno.id)
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
        user = UserFactory()
        project = ProjectFactory()
        url = reverse('project_detail', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_max_documents(self):
        """
        Ensure that a project has an max_documents property.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory(max_documents=5)
        url = reverse('project_detail', args=[project.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data['max_documents'], 5)

class TestProjectStatisticsView(APITestCase):
    def test_allowed_view(self):
        """
        Ensure project statistics can be viewed by project members.
        """
        group = GroupFactory()
        user = UserFactory(groups=[group])
        project = ProjectFactory(allowed_groups=[group])
        url = reverse('project_statistics', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deny_access_non_members(self):
        """
        Ensure users who are not project members can't view project statistics
        """
        user = UserFactory()
        project = ProjectFactory()
        url = reverse('project_statistics', args=[project.id])

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_label_distribution(self):
        """
        Ensure the response contains the current distribution of labels inside the project.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        l1 = LabelFactory(name='foo', project=project, key_code='a')
        l2 = LabelFactory(name='bar', project=project, key_code='b')
        l3 = LabelFactory(name='foobar', project=project, key_code='c')
        task = TaskFactory(project=project)
        annotations_l1 = AnnotationFactory.create_batch(20, labels=[l1], task=task)
        AnnotationFactory.create_batch(60, labels=[l2], task=task)
        AnnotationFactory.create_batch(20, labels=[l3], task=task)
        url = reverse('project_statistics', args=[project.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data['labels']['absolute']['foo'], len(annotations_l1))
        self.assertEqual(response.data['labels']['relative']['bar'], 0.6)
        self.assertEqual(response.data['labels']['total'], 100)

    def test_reviewer_labels_do_not_override_annotator(self):
        """
        Ensure that reviewer labels are not counted if there is a review task.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        l1 = LabelFactory(name='foo', project=project, key_code='a')
        l2 = LabelFactory(name='bar', project=project, key_code='b')
        l3 = LabelFactory(name='foobar', project=project, key_code='c')
        task = TaskFactory(project=project)
        task_2 = TaskFactory(project=project, action=Task.REVIEW, copied_from=task)
        anno = AnnotationFactory(task=task, labels=[l1, l2, l3])
        AnnotationFactory(task=task_2, labels=[l2, l3], copied_from=anno, action=Annotation.REVIEW)
        url = reverse('project_statistics', args=[project.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data['labels']['absolute']['foobar'], 1)
        self.assertEqual(response.data['labels']['relative']['foo'], 0.33)
        self.assertEqual(response.data['labels']['total'], 3)

    def test_task_counts(self):
        """
        Ensure that statistics contain the total count of tasks as well as absolute and percentage values for
        annotated and reviewed tasks.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        tasks_annotated = TaskFactory.create_batch(2, project=project, is_finished=True)
        TaskFactory.create_batch(2, project=project)
        tasks_reviewed = TaskFactory.create_batch(2, project=project, is_finished=True, action=Task.REVIEW)
        TaskFactory.create_batch(2, project=project, action=Task.REVIEW)
        url = reverse('project_statistics', args=[project.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data['tasks']['total'], 8)
        self.assertEqual(response.data['tasks']['annotated_absolute'], len(tasks_annotated))
        self.assertEqual(response.data['tasks']['annotated_relative'], 0.25)
        self.assertEqual(response.data['tasks']['reviewed_absolute'], len(tasks_reviewed))
        self.assertEqual(response.data['tasks']['reviewed_relative'], 0.25)

    def test_annotation_counts(self):
        """
        Ensure that statistics contain the total count of annotations as well as absolute and percentage values for
        annotated and reviewed annotations.
        """
        su = UserFactory(is_superuser=True)
        project = ProjectFactory()
        task_1 = TaskFactory(project=project, action=Task.REVIEW, is_finished=True, name="1")
        task_2 = TaskFactory(project=project, is_finished=True, name="2")
        task_3 = TaskFactory(project=project, name="3")
        AnnotationFactory.create_batch(3, task=task_1, action=Annotation.REVIEW)
        AnnotationFactory(task=task_2)
        AnnotationFactory(task=task_3)
        url = reverse('project_statistics', args=[project.id])

        self.client.force_authenticate(user=su)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data['annotations']['total'], 5)
        self.assertEqual(response.data['annotations']['annotated_absolute'], 1)
        self.assertEqual(response.data['annotations']['annotated_relative'], 0.5)
        self.assertEqual(response.data['annotations']['reviewed_absolute'], 3)
        self.assertEqual(response.data['annotations']['reviewed_relative'], 1)
    # This test works but it takes a lot of time. Updating the timings on runs and laps does not work.
    # This test can be reactivated when I figured out how to change the created_at field.
    # def test_timeseries(self):
    #     user = UserFactory.create(is_superuser=True)
    #     project = ProjectFactory.create(use_reviews=False)
    #     url = reverse('project_statistics', args=[project.id])
    #     label = LabelFactory.create(project=project)
    #     task = TaskFactory.create(annotator=user, project=project)
    #     task_unfinished = TaskFactory(annotator=user, project=project)
    #     unlabeled_annotations = AnnotationFactory.create_batch(25, task=task_unfinished)
    #     def generate_annotations(task_ref, waiting):
    #         annotations = AnnotationFactory.create_batch(25, task=task_ref)
    #         for annotation in annotations:
    #             annotation.labels.add(label)
    #             annotation.save()
    #             time.sleep(waiting)
    #         time.sleep(10)
    #         annotations[-1].labels.remove(label)
    #         annotations[-1].save()
    #     def update_timings(run, n_days, n_seconds):
    #         queryset = Run.objects.filter(id=run.id)
    #         queryset.update(created_at=run.created_at - datetime.timedelta(days=n_days))
    #         for idx, lap in enumerate(run.lap_set.all()):
    #             queryset = Lap.objects.filter(id=lap.id)
    #             queryset.update(created_at=lap.created_at - datetime.timedelta(days=n_days) + datetime.timedelta(seconds=idx * n_seconds))

    #     generate_annotations(task, 1)
    #     task.is_finished = True
    #     task.save()
    #     run = Run.objects.all().first()
    #     #update_timings(run, 1, 3)
    #     task_2 = TaskFactory(annotator=user, project=project)
    #     generate_annotations(task_2, 2)
    #     task_2.is_finished = True
    #     task_2.save()
    #     run_2 = Run.objects.filter(is_finished=False).first()
    #     print(Run.objects.all())
    #     #update_timings(run_2, 0, 5)
    #     self.client.force_authenticate(user=user)
    #     response = self.client.get(url, format='json')
    #     print(response.data)
