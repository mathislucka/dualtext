from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from dualtext_api.models import Corpus
from dualtext_api.serializers import DocumentSerializer
from dualtext_api.search.search import Search
from dualtext_api.permissions import AuthenticatedReadAdminCreate

class SearchView(APIView):
    permission = AuthenticatedReadAdminCreate()
    def get(self, request):
        if self.permission.has_permission(request, self):
            query_params = request.query_params
            corpora = query_params.getlist('corpus', None)
            methods = query_params.getlist('method', None)
            query = query_params.get('query', None)
            project = query_params.get('project', None)
            results = []
            if corpora and methods and query:
                corpora = [int(c) for c in corpora]
                if not request.user.is_superuser:
                    user_groups = request.user.groups.all()
                    corpora = Corpus.objects.filter(
                        Q(id__in=corpora) &
                        Q(allowed_groups__in=user_groups)
                    ).values_list('id', flat=True)
                s = Search(query, corpora, methods, project)
                results = DocumentSerializer(s.run(), many=True)
                results = results.data
            return Response(results)
        else:
            return Response('You need to be logged in.', status.HTTP_401_UNAUTHORIZED)

class SearchMethodsView(APIView):
    permission = AuthenticatedReadAdminCreate()
    def get(self, request):
        if self.permission.has_permission(request, self):
            methods = [key for key in Search.get_available_methods().keys()]
            return Response(methods)
        else:
            return Response('You need to be logged in.', status.HTTP_401_UNAUTHORIZED)
