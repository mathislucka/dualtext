from django.contrib.auth.models import Group
from rest_framework import generics
from dualtext_api.serializers import GroupSerializer
from dualtext_api.permissions import AdminReadOnlyPermission

class GroupListView(generics.ListAPIView):
    """
    Retrieving a list of groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AdminReadOnlyPermission]
