from rest_framework import generics
from dualtext_api.models import Project
from dualtext_api.serializers import ProjectSerializer
from dualtext_api.permissions import MembersReadAdminEdit, AuthenticatedReadAdminCreate

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
