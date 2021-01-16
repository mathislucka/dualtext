from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from .abstract_feature import AbstractFeature
import json

model = SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer')

class SentenceEmbedding(AbstractFeature):
    def __init__(self):
        self.model = model
        self.client = Elasticsearch()
        self.INDEX_NAME = 'sentence_embeddings'
    
    def create_features(self, documents):
        self.generate_and_reindex_embeddings(documents)

    def update_feature(self, document):
        embeddings = self.encode_sentences([document])
        indexable = [(document.id, embeddings[0])]
        self.update_es_index(indexable)

    def generate_and_reindex_embeddings(self, documents):
        sentences = [document.content for document in documents.all()]
        ids = [document.id for document in documents.all()]
        sentences = self.split_list(sentences, 500)
        split_ids = self.split_list(ids, 500)
        self.recreate_es_index()

        for idx, lst in enumerate(sentences):
            embeddings = self.encode_sentences(lst)
            indexable = list(zip(split_ids[idx], embeddings))
            self.update_es_index(indexable, call_refresh=False)
        self.refresh_index()

    def encode_sentences(self, sentences):
        return self.model.encode(sentences, convert_to_tensor=True)

    def process_query(self, query):
        embeddings = self.encode_sentences([query])
        return embeddings[0]
    
    def split_list(self, lst, chunk_size):
        return [lst[i * chunk_size:(i + 1) * chunk_size] for i in range((len(lst) + chunk_size - 1) // chunk_size )]
    
    def recreate_es_index(self):
        print("Creating the 'sentence_embeddings' index.")
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
                    "doc_vector": {
                        "type": "dense_vector",
                        "dims": 768
                    }
                }
            }
        }
        self.client.indices.create(index=self.INDEX_NAME, body=json.dumps(source))

    def refresh_index(self):
        self.client.indices.refresh(index=self.INDEX_NAME)

    def update_es_index(self, data, call_refresh=True):
        requests = []
        for doc_id, vector in data:
            request = {}
            request["doc_id"] = doc_id
            request["_op_type"] = "index"
            request["_index"] = self.INDEX_NAME
            request["doc_vector"] = vector.tolist()
            requests.append(request)
        bulk(self.client, requests)
        if call_refresh:
            self.refresh_index()
        print("Indexed {} documents.".format(len(data)))
