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
    
    def process_documents(self, documents):
            
        sentences = [document.content for document in documents.all()]
        ids = [document.id for document in documents.all()]
        sentences = self.split_list(sentences, 250)

        to_store = []
        # for lst in sentences:
        #     embeddings = self.model.encode(lst, convert_to_tensor=True)
        #     to_store.extend([pickle.dumps(ndarray, protocol=None, fix_imports=True, buffer_callback=None) for ndarray in embeddings])
        for lst in sentences:
            embeddings = self.model.encode(lst, convert_to_tensor=True)
            to_store.extend(embeddings)
        
        matched_embeddings = zip(ids, to_store)
        self.index_data('embeddings', matched_embeddings)
        store_rly = []
        for doc_id, emb in matched_embeddings:
            print(emb.shape)
            dump = pickle.dumps(emb, protocol=None, fix_imports=True, buffer_callback=None)
            store_rly.append((doc_id, dump))

        
        return store_rly

    def process_query(self, query):
        embeddings = self.model.encode([query])
        return embeddings[0]
    
    def split_list(self, lst, chunk_size):
        return [lst[i * chunk_size:(i + 1) * chunk_size] for i in range((len(lst) + chunk_size - 1) // chunk_size )]
    
    def index_data(self, index_name, data):
        print("Creating the 'posts' index.")
        self.client.indices.delete(index=index_name, ignore=[404])
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
        self.client.indices.create(index=index_name, body=json.dumps(source))
        
        requests = []
        for doc_id, vector in data:
            request = {}
            request["doc_id"] = doc_id
            request["_op_type"] = "index"
            request["_index"] = index_name
            request["doc_vector"] = vector.tolist()
            requests.append(request)
        bulk(self.client, requests)

        self.client.indices.refresh(index=index_name)
        print("Done indexing.")


