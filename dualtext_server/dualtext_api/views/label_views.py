from django.shortcuts import get_object_or_404
from rest_framework import generics
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

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        ls = LabelService()
        ls.create(serializer, project)
