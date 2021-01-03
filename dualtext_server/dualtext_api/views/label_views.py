from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from dualtext_api.models import Label, Project
from dualtext_api.serializers import LabelSerializer
from dualtext_api.permissions import MembersReadAdminEdit
from dualtext_api.services import LabelService

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

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'])
        ls = LabelService()
        color = ls.find_unused_color(project)
        data = request.data
        data['color'] = color
        data['project'] = project.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
