from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Prediction, Project, Annotation, Task, Document, Corpus, Label
from .serializers import LabelSerializer, TaskSerializer, ProjectSerializer, AnnotationSerializer, CorpusSerializer
from .serializers import DocumentSerializer, UserSerializer
from .permissions import TaskPermission, AnnotationPermission, MembersReadAdminEdit, AuthenticatedReadAdminCreate, DocumentPermission
from dualtext_api.search.search import Search
from dualtext_api.services.label_service import LabelService

class AnnotationListView(generics.ListCreateAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        queryset = Annotation.objects.filter(task=task)
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(Q(task__annotator=user) | Q(task__reviewer=user))
        return queryset

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        serializer.save(task=task)

class AnnotationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [AnnotationPermission]
    lookup_url_kwarg = 'annotation_id'

class CorpusListView(generics.ListCreateAPIView):
    queryset = Corpus.objects.all()
    serializer_class = CorpusSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

    def get_queryset(self):
        user = self.request.user
        queryset = Corpus.objects.all()
        if not user.is_superuser:
            user_groups = user.groups.all()
            queryset = queryset.filter(allowed_groups__in=user_groups)
        return queryset

class CorpusDetailView(generics.RetrieveDestroyAPIView):
    queryset = Corpus.objects.all()
    serializer_class = CorpusSerializer
    permission_classes = [MembersReadAdminEdit]
    lookup_url_kwarg = 'corpus_id'

class DocumentListView(generics.ListCreateAPIView):
    """
    Retrieving a list of documents in a corpus or creating new documents.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

    def get_queryset(self):
        queryset = Document.objects.filter(corpus=self.kwargs['corpus_id'])
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(corpus__allowed_groups__in=user.groups.all())
        return queryset

    def perform_create(self, serializer):
        corpus = get_object_or_404(Corpus, id=self.kwargs['corpus_id'])
        serializer.save(corpus=corpus)

class DocumentDetailView(generics.RetrieveAPIView):
    """
    Retrieving a single document.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DocumentPermission]
    lookup_url_kwarg = 'document_id'

#class GroupListView(generics.ListAPIView):


class LabelListView(generics.ListCreateAPIView):
    """
    Retrieving a list of labels in a project or creating new labels.
    """
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [MembersReadAdminEdit]
    def get_queryset(self):
        queryset = Label.objects.filter(project=self.kwargs['project_id'])
        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        ls = LabelService()
        ls.create(serializer, project)

# class LabelDetailView(generics.RetrieveUpdateDestroyAPIView):

class TaskListView(generics.ListCreateAPIView):
    """
    Retrieving a list of tasks in a project or creating new tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

    def get_queryset(self):
        queryset = Task.objects.filter(project=self.kwargs['project_id'])
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(Q(annotator=user) | Q(reviewer=user))
        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        serializer.save(project=project)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]
    lookup_url_kwarg = 'task_id'

# class PredictionListView(generics.ListCreateAPIView):

# class PredictionDetailView(generics.RetrieveUpdateDestroyAPIView):
    
class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.all()
        if not user.is_superuser:
            user_groups = user.groups.all()
            queryset = queryset.filter(allowed_groups__in=user_groups)
        return queryset

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [MembersReadAdminEdit]
    lookup_url_kwarg = 'project_id'

class SearchView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        corpora = query_params.getlist('corpus', None)
        methods = query_params.getlist('method', None)
        query = query_params.get('query', None)
        if corpora and methods and query:
            corpora = [int(c) for c in corpora]
            s = Search(query, corpora, methods)
            return s.run()
        return []

class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
