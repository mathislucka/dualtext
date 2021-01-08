from dualtext_api.models import FeatureValue
from django.db.models import Q
import json
import pickle
from sentence_transformers import util

class SentenceFarthestNeighbours():
    def __init__(self):
        self.SIMILARITY_THRESHOLD = 0.7
    
    def process_documents(self, documents):
        ids = [document.id for document in documents.all()]
        feature_values = FeatureValue.objects.filter(Q(document__id__in=ids) & Q(feature__key='sentence_embedding'))
        doc_embeddings = self.load_features(feature_values)
        far_neighbors = self.compare_to_self(doc_embeddings)
        
        return self.compare_to_stored(doc_embeddings, far_neighbors, ids)

    def compare_to_self(self, doc_embeddings):
        far_neighbors = {}
        doc_tracker = doc_embeddings
        doc_tracker.pop(0)

        for doc_id, emb in doc_embeddings:
            far_neighbors[doc_id] = {'embedding': emb, 'neighbours': []}

        for doc_id, emb in doc_embeddings:
            for sec_doc_id, sec_emb in doc_tracker:
                score = util.pytorch_cos_sim(emb, sec_emb).squeeze().tolist()
                print(score)
                if score < self.SIMILARITY_THRESHOLD:
                    far_neighbors[doc_id]['neighbours'].append(sec_doc_id)
                    far_neighbors[sec_doc_id]['neighbours'].append(doc_id)
            if len(doc_tracker) > 0:
                doc_tracker.pop(0)
        return far_neighbors
    
    def compare_to_stored(self, doc_embeddings, far_neighbors, ids):
        
        stored_neighbour_values = FeatureValue.objects.filter(~Q(document__id__in=ids) & Q(feature__key='sentence_farthest_neighbours'))
        if len(stored_neighbour_values.all()) > 0:
            stored_embedding_values = FeatureValue.objects.filter(~Q(document__id__in=ids) & Q(feature__key='sentence_embedding'))
            stored_neighbour_map = {}
            stored_embeddings = []
            for val in stored_embedding_values:
                doc_id = val.document_id
                embedding = pickle.loads(val.value, fix_imports=True, encoding="ASCII", errors="strict", buffers=None)
                feature_id = val.id
                stored_embeddings.append((doc_id, embedding, feature_id))
            for val in stored_neighbour_values:
                stored_neighbour_map[val.id] = pickle.loads(val.content, fix_imports=True, encoding="ASCII", errors="strict", buffers=None)
            
            for doc_id, emb in doc_embeddings:
                for sec_doc_id, sec_emb, feature_id in stored_embeddings:
                    score = util.pytorch_cos_sim(emb, sec_emb).squeeze().tolist()
                    if score < self.SIMILARITY_THRESHOLD:
                        far_neighbors[doc_id]['neighbours'].append(sec_doc_id)
                        stored_neighbour_map[feature_id]['neighbours'].append(doc_id)
            for val in stored_neighbour_values:
                val.value = pickle.dumps(stored_neighbour_map[val.id], protocol=None, fix_imports=True, buffer_callback=None)
                val.save()

        created_feature_values = []
        for doc_id in far_neighbors:
            print(far_neighbors[doc_id])
            content = pickle.dumps(far_neighbors[doc_id], protocol=None, fix_imports=True, buffer_callback=None)
            created_feature_values.append((doc_id, content))
        return created_feature_values

    def load_features(self, feature_values):
        doc_embeddings = []
        for fv in feature_values:
            doc_id = fv.document_id
            embedding = pickle.loads(fv.value, fix_imports=True, encoding="ASCII", errors="strict", buffers=None)
            doc_embeddings.append((doc_id, embedding))
        return doc_embeddings
