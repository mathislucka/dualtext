from rest_framework import generics
from django.shortcuts import get_object_or_404
from dualtext_api.models import AnnotationGroup, Task
from dualtext_api.serializers import AnnotationGroupSerializer
from dualtext_api.permissions import AuthenticatedReadAdminCreate, AnnotationPermission

class AnnotationGroupListView(generics.ListCreateAPIView):
    """
    Retrieving a list of annotation groups or creating new annotation groups.
    """
    queryset = AnnotationGroup.objects.all()
    serializer_class = AnnotationGroupSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

    def get_queryset(self):
        queryset = AnnotationGroup.objects.filter(task=self.kwargs['task_id']).select_related('task')
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(task__annotator=user)
        return queryset

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        serializer.save(task=task)

class AnnotationGroupDetailView(generics.RetrieveAPIView):
    """
    Retrieving a single annotation group.
    """
    queryset = AnnotationGroup.objects.all()
    serializer_class = AnnotationGroupSerializer
    permission_classes = [AnnotationPermission]
    lookup_url_kwarg = 'annotation_group_id'
