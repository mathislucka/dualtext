from sentence_transformers import SentenceTransformer
from .models import Corpus, Document, FeatureValue
from dualtext_api.feature_builders.builder import Builder
class FeatureRunner():
    def __init__(self):
        self.builder = Builder()

    def get_feature_function(self, feature_key):
        available_features = ['sentence_embedding']
        if feature_key in available_features:
            return getattr(self, feature_key)
        return None
    
    def build_feature(self, feature_key, corpus_id):
        corpus = Corpus.objects.get(id=corpus_id)
        features = corpus.feature_set
        features = features.filter(key=feature_key)
        if len(features.all()) > 0:
            documents = Document.objects.filter(corpus=corpus)
            self.builder.build_document_features(documents, feature_key)
