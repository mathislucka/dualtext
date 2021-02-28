from .abstract_search import AbstractSearch
from elasticsearch import Elasticsearch
from dualtext_api.feature_builders.elastic import Elastic
import time

class ElasticSearch(AbstractSearch):
    def __init__(self):
        self.client = Elasticsearch()
        self.elastic = Elastic()

    def search(self, corpora, excluded_documents, query):
        embedding_start = time.time()
        embedding_time = time.time() - embedding_start

        search_query = {
            "bool": { 
                "must": [
                    { "match": { "doc_content": query }}
                ],
                "filter": [
                    { "terms": { "corpus_id": corpora }}
                ],
                "must_not": [ 
                    { "terms":  { "doc_id": excluded_documents }}
                ]
            }
        }

        search_start = time.time()
        response = self.client.search(
            index=self.elastic.INDEX_NAME,
            body={
                "size": 200,
                "query": search_query,
                "_source": {"includes": ["doc_id"]}
            }
        )
        search_time = time.time() - search_start
        results = []
        print()
        print("{} total hits.".format(response["hits"]["total"]["value"]))
        print("embedding time: {:.2f} ms".format(embedding_time * 1000))
        print("search time: {:.2f} ms".format(search_time * 1000))
        for hit in response["hits"]["hits"]:
            print(hit['_score'])
            results.append((hit['_source']['doc_id'], hit['_score'], 'elastic'))

        return results