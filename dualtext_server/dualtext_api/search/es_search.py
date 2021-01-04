from elasticsearch_dsl import Q
from ..documents import DocumentDocument

class ElasticSearch():
    def search(self, documents, query):
        if query == '':
            return []
        search = DocumentDocument.search()
        search = search.filter('terms', id=documents)
        search = search.query("match", content=query)

        return [(hit.id, hit.meta.score, 'elastic') for hit in search]
