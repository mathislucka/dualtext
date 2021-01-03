from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from dualtext_api.models import Task, Project
from dualtext_api.serializers import TaskSerializer
from dualtext_api.permissions import TaskPermission, AuthenticatedReadAdminCreate, MembersReadAdminEdit, MembersEdit
from dualtext_api.services import ProjectService

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

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'])
        data = request.data
        data['project'] = project.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieving a single task updating an existing task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]
    lookup_url_kwarg = 'task_id'

class ClaimTaskView(APIView):
    """
    Claiming an unclaimed task.
    """
    def get(self, request, project_id):
        out = {}
        project = get_object_or_404(Project, id=project_id)
        permission = MembersReadAdminEdit()

        if permission.has_object_permission(request, self, project):
            ps = ProjectService(project_id)
            open_annotation_tasks = ps.get_open_annotation_tasks().count()
            open_review_tasks = ps.get_open_review_tasks().count()
            out['open_reviews'] = open_review_tasks
            out['open_annotations'] = open_annotation_tasks
            return Response(out)
        return Response('You are not permitted to access this resource.', status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, project_id, claim_type):
        project = get_object_or_404(Project, id=project_id)
        serializer = TaskSerializer
        permission = MembersEdit()
        
        if permission.has_object_permission(request, self, project):
            task = None
            ps = ProjectService(project_id)
            if claim_type == 'annotation':
                task = ps.claim_annotation_task(request.user)
            elif claim_type == 'review':
                task = ps.claim_review_task(request.user)
        
            if task is not None:
                return Response(serializer(task).data)
            else:
                return Response('There is no task to claim', status=status.HTTP_409_CONFLICT)
        return Response('You are not permitted to access this resource', status=status.HTTP_403_FORBIDDEN)