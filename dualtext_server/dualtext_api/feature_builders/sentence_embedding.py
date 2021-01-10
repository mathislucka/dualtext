from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from dualtext_api.models import FeatureValue, Feature
import pickle
import json

model = SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer')

class SentenceEmbedding():
    def __init__(self):
        self.model = model
        self.client = Elasticsearch()
        self.INDEX_NAME = 'sentence_embeddings'
    
    def create_feature(self, documents):
        embeddings = self.generate_embeddings(documents)
        #return self.save_feature(embeddings)

    
    def update_feature(self, documents):
        embeddings = self.generate_embeddings(documents)
        self.update_es_index(embeddings)
        return self.prepare_for_storage(embeddings)

    def generate_embeddings(self, documents):
        sentences = [document.content for document in documents.all()]
        ids = [document.id for document in documents.all()]
        sentences = self.split_list(sentences, 500)
        split_ids = self.split_list(ids, 500)
        self.recreate_es_index()

        # embeddings = self.model.encode([sentences[0][0]])
        # ids = [ids[0]]
        # for emb in embeddings:
        #     print(emb.shape)

        for idx, lst in enumerate(sentences):
            embeddings = self.model.encode(lst, convert_to_tensor=True)
            storable = list(zip(split_ids[idx], embeddings))
            self.update_es_index(storable)
            #self.save_feature(storable)
    
    def save_feature(self, embeddings):
        feature = Feature.objects.get(key='sentence_embedding')
        values_to_save = []
        for doc_id, emb in embeddings:
            dump = pickle.dumps(emb, protocol=None, fix_imports=True, buffer_callback=None)
            feature_value = FeatureValue(value=dump, feature=feature)
            feature_value.document_id = doc_id
            values_to_save.append(feature_value)
        FeatureValue.objects.bulk_create(values_to_save)
            

    def process_query(self, query):
        embeddings = self.model.encode([query], convert_to_tensor=True)
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
    
    def build_es_index(self, data):
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
        self.update_es_index(data)
        #self.client.indices.refresh(index=self.INDEX_NAME)
    
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
            self.client.indices.refresh(index=self.INDEX_NAME)
        print("Done indexing.")


