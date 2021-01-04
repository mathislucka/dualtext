from django.db.models import Q
from sentence_transformers import util
import pickle
from ..models import Document, FeatureValue
from dualtext_api.feature_builders.sentence_embedding import SentenceEmbedding
class SentenceEmbeddingSearch():
    def search(self, documents, query):
        sent_embed = SentenceEmbedding()
        embedded_query = sent_embed.process_query(query)
        features_values = FeatureValue.objects.filter(Q(document__id__in=documents) & Q(feature__key='sentence_embedding'))
        results = []
        for fv in features_values:
            doc_id = fv.document_id
            embedding = pickle.loads(fv.value, fix_imports=True, encoding="ASCII", errors="strict", buffers=None)
            score = util.pytorch_cos_sim(embedded_query, embedding).squeeze().tolist()
            results.append((doc_id, score, 'sentence_embedding'))
        results = sorted(results, key=lambda tup: tup[1], reverse=True)
        return results