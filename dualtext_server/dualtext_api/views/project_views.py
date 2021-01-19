from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from dualtext_api.models import Project
from dualtext_api.serializers import ProjectSerializer
from dualtext_api.permissions import MembersReadAdminEdit, AuthenticatedReadAdminCreate
from dualtext_api.services import ProjectService

class ProjectListView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.all().prefetch_related('corpora', 'allowed_groups')
        print(queryset.explain())
        if not user.is_superuser:
            user_groups = user.groups.all()
            queryset = queryset.filter(allowed_groups__in=user_groups)
        return queryset

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [MembersReadAdminEdit]
    lookup_url_kwarg = 'project_id'

class ProjectStatisticsView(APIView):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        permission = MembersReadAdminEdit()

        if permission.has_object_permission(request, self, project):
            ps = ProjectService(project_id)
            statistics = ps.get_project_statistics()
            return Response(statistics)
        return Response('not permitted', status=status.HTTP_403_FORBIDDEN)
