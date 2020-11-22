from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Project, Label, Task, Annotation, Document, Corpus

def run_standard_setup():
    superuser = User(username="superuser", is_superuser = True, password='pass')
    superuser.save()
    group = Group(name='project_members')
    group.save()
    user = User(username="normal", password="pass")
    user.save()
    user.groups.add(group)
    user.save()
    project = Project(name="TestProject", creator=superuser)
    project.save()
    project.allowed_groups.add(group)
    project.save()
    return {'project': project, 'superuser': superuser, 'group': group, 'user': user}

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(Label.objects.get(id=1).name, 'TestLabel')
        self.assertEqual(Label.objects.get().project, self.project)
    
    def test_superuser_view(self):
        """
        Ensure superusers can always view labels.
        """
        label = Label(name='TestLabel', project=self.project)
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
        label = Label(name='TestLabel', project=self.project)
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
        l1 = Label(name="TestLabel", project=self.project)
        l1.save()
        l2 = Label(name="Second", project=p2)
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

class TestAnnotationListView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']
        task = Task(name='Task 1', annotator=self.user, project=self.project)
        task.save()
        self.task = task

        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('annotation_list', args=[self.task.id])
    
    def test_creation(self):
        """
        Ensure a new annotation can be created by a superuser.
        """
        data = {'documents': [self.document.id], 'corpus': [self.corpus.id]}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Annotation.objects.count(), 1)
        self.assertEqual(Annotation.objects.get(id=1).documents.all()[0], self.document)
        self.assertEqual(Annotation.objects.get(id=1).task, self.task)

    def test_superuser_view(self):
        """
        Ensure a superuser can view all annotations.
        """
        a1 = Annotation(task=self.task)
        a1.save()
        a1.documents.add(self.document)
        a1.save()

        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['documents'], [self.document.id])
        self.assertEqual(response.data[0]['task'], self.task.id)

    def test_view_only_allowed(self):
        """
        Ensure users can only view annotations that are children of tasks where the user is assigned as annotator or reviewer.
        """
        t2 = Task(annotator=self.superuser, reviewer=self.user, project=self.project, name='Reviewer Task')
        t2.save()
        t3 = Task(annotator=self.superuser, project=self.project, name='Not assigned task')
        t3.save()
        
        a1 = Annotation(task=self.task)
        a1.save()
        a1.documents.add(self.document)
        a1.save()

        a2 = Annotation(task=t2)
        a2.save()
        a2.documents.add(self.document)
        a2.save()

        a3 = Annotation(task=t3)
        a3.save()
        a3.documents.add(self.document)
        a3.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        response_2 = self.client.get(reverse('annotation_list', args=[t2.id]))
        response_3 = self.client.get(reverse('annotation_list', args=[t3.id]))

        response_2_task = Task.objects.get(id=response_2.data[0]['task'])
        response_task = Task.objects.get(id=response.data[0]['task'])
        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response_task.annotator, self.user)
        
        self.assertEqual(len(response_2.data), 1)
        self.assertEqual(response_2_task.reviewer, self.user)

        self.assertEqual(len(response_3.data), 0)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create annotations.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestAnnotationDetailView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']
        
        task = Task(name='Task 1', annotator=self.user, project=self.project)
        task.save()
        self.task = task
        
        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        annotation = Annotation(task=self.task)
        annotation.save()
        annotation.documents.add(self.document)
        annotation.save()
        self.annotation = annotation

        self.url = reverse('annotation_detail', args=[self.task.id, self.annotation.id])
    
    def test_reviewer_annotator_view(self):
        """
        Ensure that reviewers and annotators of a task can view an annotation.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        response_task_id = response.data['task']
        self.assertEqual(response_task_id, self.task.id)
        self.assertEqual(Task.objects.get(id=response_task_id).annotator, self.user)

        self.task.annotator = self.superuser
        self.task.reviewer = self.user
        self.task.save()

        response_2 = self.client.get(self.url, format='json')
        response_2_task_id = response_2.data['task']
        self.assertEqual(response_2_task_id, self.task.id)
        self.assertEqual(Task.objects.get(id=response_2_task_id).reviewer, self.user)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all annotations.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.annotation.id)
        self.assertEqual(response.data['task'], self.task.id)
    
    def test_reviewer_annotator_edit(self):
        """
        Ensure that reviewers and annotators can edit an annotation.
        """
        label = Label(name="annotator", project=self.project)
        label.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {'annotator_labels': [label.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Annotation.objects.get(id=response.data['id']).annotator_labels.all()[0], label)

        self.task.annotator = self.superuser
        self.task.reviewer = self.user
        self.task.save()

        response_2 = self.client.patch(self.url, {'reviewer_labels': [label.id]}, format='json')
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(Annotation.objects.get(id=response_2.data['id']).reviewer_labels.all()[0], label)

    def test_superuser_edit(self):
        """
        Ensure that superusers can edit an annotation.
        """
        label = Label(name="annotator", project=self.project)
        label.save()

        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(self.url, {'annotator_labels': [label.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Annotation.objects.get(id=response.data['id']).annotator_labels.all()[0], label)

    def test_deny_non_reviewer_annotator_view(self):
        """
        Ensure that users who are neither annotator nor reviewer can't see an annotation.
        """
        self.task.annotator = self.superuser
        self.task.reviewer = self.superuser
        self.task.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_non_reviewer_annotator_edit(self):
        """
        Ensure that users who are neither annotator nor reviewer can't edit an annotation.
        """
        self.task.annotator = self.superuser
        self.task.reviewer = self.superuser
        self.task.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestCorpusListView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.url = reverse('corpus_list')
    
    def test_creation(self):
        """
        Ensure a new corpus can be created by a superuser.
        """
        data = {'name': 'Test Corpus', 'corpus_meta': { 'info': 'corpus info'}}
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Corpus.objects.count(), 1)
        self.assertEqual(Corpus.objects.get(id=response.data['id']).name, 'Test Corpus')
        self.assertEqual(Corpus.objects.get(id=response.data['id']).corpus_meta, {'info': 'corpus info'})

    def test_superuser_view(self):
        """
        Ensure a superuser can view all corpora.
        """
        corpus = Corpus(name='Foo', corpus_meta={})
        corpus.save()
        
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], corpus.name)

    def test_view_only_allowed(self):
        """
        Ensure users can only view corpora that they are allowed to see.
        """
        corpus = Corpus(name='Foo', corpus_meta={})
        corpus.save()
        corpus.allowed_groups.add(self.group)
        corpus.save()
        self.user.groups.add(self.group)
        self.user.save()
        corpus_2 = Corpus(name='Bar', corpus_meta={})
        corpus_2.save()
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], corpus.name)

    def test_deny_creation_non_superuser(self):
        """
        Ensure only superuser can create corpora.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestCorpusDetailView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        self.project = standards['project']
        
        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('corpus_detail', args=[self.corpus.id])
    
    def test_allowed_view(self):
        """
        Ensure that users can view a corpus that they are allowed to view.
        """
        self.corpus.allowed_groups.add(self.group)
        self.corpus.save()
        self.user.groups.add(self.group)
        self.user.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.corpus.id)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all corpora.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.corpus.id)

    def test_superuser_delete(self):
        """
        Ensure that superusers can delete a corpus.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.url, format='json')
        try:
            corpus = Corpus.objects.get(id=1)
        except Corpus.DoesNotExist:
            corpus = None

        try:
            document = Document.objects.get(id=1)
        except Document.DoesNotExist:
            document = None

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(corpus, None)
        self.assertEqual(document, None)

    def test_deny_non_member_view(self):
        """
        Ensure that users who are not allowed to view a corpus can't view it.
        """
        self.user.groups.remove(self.group)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deny_non_superuser_delete(self):
        """
        Ensure that users who are not superusers can't delete a corpus.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestDocumentListView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        
        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('document_list', args=[self.corpus.id])
    
    def test_allowed_view(self):
        """
        Ensure that users can view documents that they are allowed to view.
        """
        self.corpus.allowed_groups.add(self.group)
        self.corpus.save()
        self.user.groups.add(self.group)
        self.user.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], self.document.content)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all documents.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], self.document.content)

class TestDocumentDetailView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        
        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('document_detail', args=[self.corpus.id, self.document.id])
    
    def test_allowed_view(self):
        """
        Ensure that users can view documents that they are allowed to view.
        """
        self.corpus.allowed_groups.add(self.group)
        self.corpus.save()
        self.user.groups.add(self.group)
        self.user.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.document.content)

    def test_superuser_view(self):
        """
        Ensure that superusers can see all documents.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.document.content)
    
    def deny_not_allowed_view(self):
        """
        Ensure that users can only view a document that they are allowed to view.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestSearchView(APITestCase):
    def setUp(self):
        standards = run_standard_setup()
        self.user = standards['user']
        self.superuser = standards['superuser']
        self.group = standards['group']
        
        corpus = Corpus(name='New Corpus', corpus_meta={})
        corpus.save()
        self.corpus = corpus

        document = Document(content='A new document', corpus=self.corpus)
        document.save()
        self.document = document

        self.url = reverse('search')
    def test_search(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.get(self.url + '?search=document')
        print(response.data)