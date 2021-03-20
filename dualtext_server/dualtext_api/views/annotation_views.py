import random
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from dualtext_api.models import Annotation, Task
from dualtext_api.serializers import AnnotationSerializer, LabelSerializer
from dualtext_api.permissions import AnnotationPermission, AuthenticatedReadAdminCreate
from dualtext_api.services import ProjectService, RunService
from dualtext_api.filters import AnnotationFilter


class AnnotationListView(APIView):
    def get(self, request, task_id):
        serializer = AnnotationSerializer
        permission = AuthenticatedReadAdminCreate
        if AuthenticatedReadAdminCreate().has_permission(request, self):
            task = get_object_or_404(Task, id=task_id)
            queryset = Annotation.objects.filter(task=task).select_related('task').prefetch_related('documents', 'labels')
            user = request.user
            if not user.is_superuser:
                queryset = queryset.filter(task__annotator=user)
            ps = ProjectService(task.project_id)
            desired_label = ps.get_desired_label()
            queryset = AnnotationFilter(data=request.GET, queryset=queryset).qs
            data = AnnotationSerializer(queryset, many=True).data
            if desired_label:
                for annotation in data:
                    annotation['desired_label'] = LabelSerializer(desired_label[random.randrange(0, len(desired_label))]).data
            return Response(data)
        return Response('You must be logged in to request this resource.', status.HTTP_401_UNAUTHORIZED)


    def post(self, request, task_id):
        serializer = AnnotationSerializer
        permission = AuthenticatedReadAdminCreate
        if AuthenticatedReadAdminCreate().has_permission(request, self):
            task = get_object_or_404(Task, id=task_id)
            serialized = AnnotationSerializer(data=request.data)
            serialized.is_valid(raise_exception=True)
            serialized.save(task=task)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response('You are not permitted to access this resource.', status.HTTP_403_FORBIDDEN)

class AnnotationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    permission_classes = [AnnotationPermission]
    lookup_url_kwarg = 'annotation_id'

    def update(self, request, *args, **kwargs):
        annotation_id = kwargs['annotation_id']
        annotation = get_object_or_404(Annotation, id=annotation_id)
        labels = set(annotation.labels.values_list("id", flat=True))
        documents = set(annotation.documents.values_list("id", flat=True))
        new_documents = request.data.get('documents', None)
        new_labels = request.data.get('labels', None)
        documents_changed = False
        labels_changed = False
        if new_labels is not None:
            new_labels = set([int(l) for l in new_labels])
            labels_changed = new_labels != labels

        if new_documents is not None:
            new_documents = set([int(d) for d in new_documents])
            documents_changed = new_documents != documents

        if documents_changed or labels_changed:
            task = annotation.task
            rs = RunService(task)
            rs.log_lap(annotation)

        return super(AnnotationDetailView, self).update(request, *args, **kwargs)
