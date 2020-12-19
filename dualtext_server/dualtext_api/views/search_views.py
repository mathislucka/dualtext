from rest_framework import generics
from dualtext_api.models import Document
from dualtext_api.serializers import DocumentSerializer
from dualtext_api.search.search import Search

class SearchView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        corpora = query_params.getlist('corpus', None)
        methods = query_params.getlist('method', None)
        query = query_params.get('query', None)
        if corpora and methods and query:
            corpora = [int(c) for c in corpora]
            s = Search(query, corpora, methods)
            return s.run()
        return []