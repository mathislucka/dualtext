from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from dualtext_api.models import Annotation, Task
from dualtext_api.serializers import AnnotationSerializer
from dualtext_api.permissions import AnnotationPermission, AuthenticatedReadAdminCreate
from dualtext_api.services import ProjectService


class AnnotationListView(APIView):
    def get(self, request, task_id):
        serializer = AnnotationSerializer
        permission = AuthenticatedReadAdminCreate
        if AuthenticatedReadAdminCreate().has_permission(request, self):
            task = get_object_or_404(Task, id=task_id)
            queryset = Annotation.objects.filter(task=task)
            user = request.user
            if not user.is_superuser:
                queryset = queryset.filter(Q(task__annotator=user) | Q(task__reviewer=user))
            ps = ProjectService(task.project.id)
            desired_label = ps.get_desired_label()
            data = AnnotationSerializer(queryset, many=True).data
            # for annotation in data:
            #     annotation['desired_label'] = desired_label
            return Response(data)
        return Response('You are not permitted to access this resource.', status.HTTP_403_FORBIDDEN)


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
