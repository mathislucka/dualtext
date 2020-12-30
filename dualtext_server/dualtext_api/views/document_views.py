from django.shortcuts import get_object_or_404
from rest_framework import generics
from dualtext_api.models import Corpus, Document
from dualtext_api.serializers import DocumentSerializer
from dualtext_api.permissions import DocumentPermission, AuthenticatedReadAdminCreate

class DocumentListView(generics.ListCreateAPIView):
    """
    Retrieving a list of documents in a corpus or creating new documents.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

    def get_queryset(self):
        queryset = Document.objects.filter(corpus=self.kwargs['corpus_id'])
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(corpus__allowed_groups__in=user.groups.all())
        return queryset

    def perform_create(self, serializer):
        corpus = get_object_or_404(Corpus, id=self.kwargs['corpus_id'])
        serializer.save(corpus=corpus)

class DocumentDetailView(generics.RetrieveAPIView):
    """
    Retrieving a single document.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DocumentPermission]
    lookup_url_kwarg = 'document_id'