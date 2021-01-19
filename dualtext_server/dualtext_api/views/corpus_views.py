from django.db.models import Count
from rest_framework import generics
from dualtext_api.models import Corpus
from dualtext_api.serializers import CorpusSerializer
from dualtext_api.permissions import MembersReadAdminEdit, AuthenticatedReadAdminCreate

class CorpusListView(generics.ListCreateAPIView):
    serializer_class = CorpusSerializer
    permission_classes = [AuthenticatedReadAdminCreate]

    def get_queryset(self):
        user = self.request.user
        queryset = Corpus.objects.annotate(Count('document')).all().prefetch_related('allowed_groups')
        if not user.is_superuser:
            user_groups = user.groups.all()
            queryset = queryset.filter(allowed_groups__in=user_groups)
        return queryset

class CorpusDetailView(generics.RetrieveDestroyAPIView):
    queryset = Corpus.objects.all()
    serializer_class = CorpusSerializer
    permission_classes = [MembersReadAdminEdit]
    lookup_url_kwarg = 'corpus_id'
