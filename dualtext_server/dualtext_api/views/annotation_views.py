from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics
from dualtext_api.models import Annotation, Task
from dualtext_api.serializers import AnnotationSerializer
from dualtext_api.permissions import AnnotationPermission, AuthenticatedReadAdminCreate


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
