from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pickle
import json

model = SentenceTransformer('distilbert-multilingual-nli-stsb-quora-ranking')

class SentenceEmbedding():
    def __init__(self):
        self.model = model
        self.client = Elasticsearch()
        self.INDEX_NAME = 'sentence_embeddings'
    
    def create_feature(self, documents):
        embeddings = self.generate_embeddings(documents)
        self.index_data(embeddings)
        return self.prepare_for_storage(embeddings)

    
    def update_feature(self, documents):
        embeddings = self.generate_embeddings(documents)
        self.update_es_index(embeddings)
        return self.prepare_for_storage(embeddings)

    def generate_embeddings(self, documents):
        sentences = [document.content for document in documents.all()]
        ids = [document.id for document in documents.all()]
        sentences = self.split_list(sentences, 250)

        generated = []
        for lst in sentences:
            embeddings = self.model.encode(lst, convert_to_tensor=True)
            generated.extend(embeddings)
        
        return zip(ids, generated)
    
    def prepare_for_storage(self, embeddings):
        to_store = []
        for doc_id, emb in matched_embeddings:
            dump = pickle.dumps(emb, protocol=None, fix_imports=True, buffer_callback=None)
            to_store.append((doc_id, dump))
        return to_store


    def process_query(self, query):
        embeddings = self.model.encode([query])
        return embeddings[0]
    
    def split_list(self, lst, chunk_size):
        return [lst[i * chunk_size:(i + 1) * chunk_size] for i in range((len(lst) + chunk_size - 1) // chunk_size )]
    
    def build_es_index(self, data):
        print("Creating the 'posts' index.")
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
        self.update_es_index(data)
    
    def update_es_index(self, data):
        requests = []
        for doc_id, vector in data:
            request = {}
            request["doc_id"] = doc_id
            request["_op_type"] = "index"
            request["_index"] = self.INDEX_NAME
            request["doc_vector"] = vector.tolist()
            requests.append(request)
        bulk(self.client, requests)

        self.client.indices.refresh(index=self.INDEX_NAME)
        print("Done indexing.")


