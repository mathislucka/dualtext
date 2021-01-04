from django.shortcuts import get_object_or_404
from rest_framework import generics
from dualtext_api.models import Corpus, Feature
from dualtext_api.serializers import FeatureSerializer
from dualtext_api.permissions import MembersReadAdminEdit

class FeatureListView(generics.ListCreateAPIView):
    """
    Retrieving a list of features of a corpus or creating new features.
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [MembersReadAdminEdit]

    def get_queryset(self):
        queryset = Feature.objects.filter(corpus=self.kwargs['corpus_id'])
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(corpus__allowed_groups__in=user.groups.all())
        return queryset

    def perform_create(self, serializer):
        corpus = get_object_or_404(Corpus, id=self.kwargs['corpus_id'])
        serializer.save(corpus=corpus)
