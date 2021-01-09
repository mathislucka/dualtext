from django.db.models import Case, When, Q
from ..models import Document, Project
from .es_search import ElasticSearch
from .sentence_embedding_search import SentenceEmbeddingSearch
from .boost_search import BoostSearch
from dualtext_api.services import ProjectService

class Search():
    def __init__(self, query, corpora, methods, project_id):
        self.query = query
        self.corpora = corpora
        self.methods = methods
        self.available_methods = {
            'elastic': ElasticSearch,
            'sentence_embedding': SentenceEmbeddingSearch
        }
        self.project_id = None
        if project_id:
            self.project_id = int(project_id)

    def run(self):
        results = []
        documents = self.get_documents()
        for method in self.methods:
            s = self.available_methods[method]()
            s = s.search(documents, self.query)
            results.extend(s)
        return self.postprocess_results(results)

    def postprocess_results(self, results):
        sorted_ids = sorted(results, key=lambda tup: tup[1], reverse=True)
        seen = set()
        unique_ids = []
        methods = []
        for doc_id, _, method in sorted_ids:
            if not doc_id in seen:
                seen.add(doc_id)
                unique_ids.append(doc_id)
                methods.append(method)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(unique_ids)])
        queryset = Document.objects.filter(pk__in=unique_ids).order_by(preserved)
        for idx, q in enumerate(queryset):
            q.method = methods[idx]
        return queryset

    def get_documents(self):
        project = None
        if self.project_id:
            project = Project.objects.get(id=self.project_id)

        if project and project.annotation_document_duplicates == False:
            ps = ProjectService(self.project_id)
            annotations = ps.get_total_annotations().values_list('id', flat=True)
            document_queryset = Document.objects.filter(Q(corpus__id__in=self.corpora) & ~Q(annotation__id__in=annotations))
        else:
            document_queryset = Document.objects.filter(corpus__id__in=self.corpora)

        return list(document_queryset.values_list('id', flat=True))



