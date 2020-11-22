from django.db.models import Case, When
from ..models import Document
from .es_search import ElasticSearch
from .sentence_embedding_search import SentenceEmbeddingSearch

class Search():
    def __init__(self, query, corpora, methods):
        self.query = query
        self.corpora = corpora
        self.methods = methods
        self.available_methods = {
            'elastic': ElasticSearch,
            'sentence_embedding': SentenceEmbeddingSearch
        }
    def run(self):
        results = []
        for method in self.methods:
            s = self.available_methods[method]()
            s = s.search(self.corpora, self.query)
            results.extend(s)
        return self.postprocess_results(results)
    
    def postprocess_results(self, results):
        sorted_ids = sorted(results, key=lambda tup: tup[1], reverse=True)
        print('The sorted results are {}.'.format(sorted_ids))
        seen = set()
        unique_ids = []
        methods = []
        for doc_id, _, method in sorted_ids:
            if not doc_id in seen:
                seen.add(doc_id)
                unique_ids.append(doc_id)
                methods.append(method)
        print('The unique_ids are {}.'.format(unique_ids))
        print('The methods are {}.'.format(methods))
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(unique_ids)])
        queryset = Document.objects.filter(pk__in=unique_ids).order_by(preserved)
        for idx, q in enumerate(queryset):
            q.method = methods[idx]
        return queryset
