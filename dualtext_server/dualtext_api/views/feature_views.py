from django.shortcuts import get_object_or_404
from rest_framework import generics
from dualtext_api.models import Corpus, Feature
from dualtext_api.serializers import FeatureSerializer
from dualtext_api.permissions import AuthenticatedReadAdminCreate

class FeatureListView(generics.ListCreateAPIView):
    """
    Retrieving a list of features or creating new features.
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

class FeatureDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieving or updating a single feature.
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [AuthenticatedReadAdminCreate]
    lookup_url_kwarg = 'feature_id'