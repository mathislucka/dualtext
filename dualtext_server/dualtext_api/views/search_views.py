from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from dualtext_api.models import Corpus, Document
from dualtext_api.serializers import DocumentSerializer
from dualtext_api.permissions import AuthenticatedReadAdminCreate
from dualtext_api.haystack_documents import DualtextDocument
from dualtext_api.haystack_connector.pipelines import initialized_pipelines
from dualtext_api.services.search_service import SearchService


class SearchView(APIView):
    permission = AuthenticatedReadAdminCreate()

    def get(self, request):
        if not self.permission.has_permission(request, self):
            return Response('You need to be logged in.', status.HTTP_401_UNAUTHORIZED)

        query_params = request.query_params
        corpus = query_params.get('corpus', None)
        method = query_params.get('method', None)
        query = query_params.get('query', None)
        project = query_params.get('project', None)

        if corpus and method and query:
            user_groups = request.user.groups.values_list('id', flat=True)
            corpus_id = int(corpus)
            corpus = Corpus.objects.get(id=corpus_id)
            corpus_allowed_groups = corpus.allowed_groups.values_list('id', flat=True)

            if set(user_groups).isdisjoint(set(corpus_allowed_groups)) and not request.user.is_superuser:
                return Response('You are not permitted to access this resource.', status=status.HTTP_403_FORBIDDEN)

            query_set = DualtextDocument.query_pipeline(pipeline_name=method)
            results = query_set.query(query).set_options(index=corpus_id).run()
            search_service = SearchService(corpus_id=corpus_id, project_id=int(project) if project else None)
            results = search_service.postprocess_results(results=results, search_method=method)
            results = DocumentSerializer(results, many=True)
            results = results.data

            return Response(results)
        else:
            return Response('Missing search parameters', status.HTTP_400_BAD_REQUEST)


class SearchMethodsView(APIView):
    permission = AuthenticatedReadAdminCreate()
    def get(self, request):
        if self.permission.has_permission(request, self):
            methods = list(initialized_pipelines['query'].keys())
            return Response(methods)
        else:
            return Response('You need to be logged in.', status.HTTP_401_UNAUTHORIZED)
