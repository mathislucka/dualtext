from elasticsearch_dsl import Q
from ..documents import DocumentDocument

class ElasticSearch():
    def search(self, corpora, query):
        if query == '':
            return []
        search = DocumentDocument.search()
        search = search.filter('nested', path='corpus', query=Q('terms', corpus__id=corpora))
        search = search.query("match", content=query)

        return [(hit.id, hit.meta.score, 'elastic') for hit in search]
