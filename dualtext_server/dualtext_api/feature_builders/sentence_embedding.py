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
        self.BATCH_SIZE = 700
    
    def create_features(self, documents):
        if not self.client.indices.exists(index=self.INDEX_NAME):
            self.recreate_es_index()
        self.generate_and_reindex_embeddings(documents)

    def update_feature(self, documents):
        sentences = [d.content for d in documents]
        ids = [(d.id, d.corpus.id) for d in documents]
        embeddings = self.encode_sentences(sentences)
        indexable = list(zip(ids, embeddings))
        self.update_es_index(indexable)
    
    def remove_features(self, documents):
        documents = [doc.id for doc in documents]
        self.client.delete_by_query(index=self.INDEX_NAME, body={"query": {"terms": {"doc_id": documents}}})
        self.refresh_index()

    def generate_and_reindex_embeddings(self, documents):
        split_documents = self.split_list(documents, self.BATCH_SIZE)
        for docs in split_documents:
            self.remove_features(docs)
        sentences = [document.content for document in documents.all()]
        ids = [(document.id, document.corpus.id) for document in documents.all()]
        sentences = self.split_list(sentences, self.BATCH_SIZE)
        split_ids = self.split_list(ids, self.BATCH_SIZE)

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
                    "corpus_id": {
                        "type": "keyword"
                    },
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
        for doc, vector in data:
            request = {}
            request["corpus_id"] = doc[1]
            request["doc_id"] = doc[0]
            request["_op_type"] = "index"
            request["_index"] = self.INDEX_NAME
            request["doc_vector"] = vector.tolist()
            requests.append(request)
        bulk(self.client, requests)
        if call_refresh:
            self.refresh_index()
        print("Indexed {} documents.".format(len(data)))
