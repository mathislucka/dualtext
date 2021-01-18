from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from .abstract_feature import AbstractFeature
import json

class Elastic(AbstractFeature):
    def __init__(self):
        self.client = Elasticsearch()
        self.INDEX_NAME = 'documentas'
    
    def create_features(self, documents):
        self.reindex_documents(documents)

    def update_feature(self, documents):
        self.update_index(documents)
    
    def remove_features(self, documents):
        documents = [doc.id for doc in documents]
        print(documents)
        self.client.delete_by_query(index=self.INDEX_NAME, body={"query": {"terms": {"doc_id": documents}}})
        self.refresh_index()

    def reindex_documents(self, documents):
        split_documents = self.split_list(documents, 500)
        self.recreate_es_index()

        for doc_chunk in split_documents:
            self.update_es_index(doc_chunk, call_refresh=False)
        self.refresh_index()

    def process_query(self, query):
        pass
    
    def split_list(self, lst, chunk_size):
        return [lst[i * chunk_size:(i + 1) * chunk_size] for i in range((len(lst) + chunk_size - 1) // chunk_size )]
    
    def recreate_es_index(self):
        print("Creating the 'elastic' index.")
        self.client.indices.delete(index=self.INDEX_NAME, ignore=[404])
        source = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1
            },
            "mappings": {
                "dynamic": "true",
                "_source": {
                    "enabled": "true"
                },
                "properties": {
                    "doc_id": {
                        "type": "keyword"
                    },
                    "doc_content": {
                        "type": "text"
                    }
                }
            }
        }
        self.client.indices.create(index=self.INDEX_NAME, body=json.dumps(source))

    def refresh_index(self):
        self.client.indices.refresh(index=self.INDEX_NAME)

    def update_index(self, data, call_refresh=True):
        exists = self.client.indices.exists([self.INDEX_NAME])
        if exists == False:
            self.recreate_es_index()
        requests = []
        print(data)
        if len(data) > 0:
            self.remove_features(data)
        for doc in data:
            request = {}
            request["doc_id"] = doc.id
            request["_op_type"] = "index"
            request["_index"] = self.INDEX_NAME
            request["doc_content"] = doc.content
            requests.append(request)
        bulk(self.client, requests)
        if call_refresh:
            self.refresh_index()
        print("Indexed {} documents.".format(len(data)))
