from .abstract_search import AbstractSearch
from dualtext_api.feature_builders.sentence_embedding import SentenceEmbedding
from elasticsearch import Elasticsearch
import time

class SentenceEmbeddingSearch(AbstractSearch):
    def __init__(self):
        self.SIMILARITY_THRESHOLD = 1.2
        self.client = Elasticsearch()

    def search(self, corpora, excluded_documents, query):
        embedding_start = time.time()
        sent_embed = SentenceEmbedding()
        embedded_query = sent_embed.process_query(query).tolist()
        embedding_time = time.time() - embedding_start

        script_query = {
            "script_score": {
                "query": {
                    "bool": { 
                        "filter": [
                            { "terms": { "corpus_id": corpora }}
                        ],
                        "must_not": [ 
                            { "terms":  { "doc_id": excluded_documents }}
                        ]
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'doc_vector') + 1.0",
                    "params": {"query_vector": embedded_query}
                }
            }
        }

        search_start = time.time()
        response = self.client.search(
            index=sent_embed.INDEX_NAME,
            body={
                "size": 200,
                "query": script_query,
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
            if hit['_score'] > self.SIMILARITY_THRESHOLD:
                results.append((hit['_source']['doc_id'], hit['_score'], 'sentence_embedding'))

        return results