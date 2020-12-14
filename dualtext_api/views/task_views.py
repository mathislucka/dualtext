from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics
from dualtext_api.models import Task, Project
from dualtext_api.serializers import TaskSerializer
from dualtext_api.permissions import TaskPermission, AuthenticatedReadAdminCreate

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
    """
    Retrieving a single task updating an existing task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]
    lookup_url_kwarg = 'task_id'
