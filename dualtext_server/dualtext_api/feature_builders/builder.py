from .sentence_embedding import SentenceEmbedding
from django.db.models import Q
from ..models import Corpus, Document, FeatureValue

class Builder():
    def __init__(self):
        self.features = {'sentence_embedding': SentenceEmbedding(),}

    def build_document_features(self, documents, feature_key):
        print('starting to build {} for {} documents...'.format(feature_key, len(documents.all())))
        stale_feature_values = FeatureValue.objects.filter(Q(document__in=documents) & Q(feature__key=feature_key)).delete()
        print('removed {} stale feature values'.format(stale_feature_values[0]))

        feature_instance = self.features.get(feature_key, None)
        if feature_instance is not None:
            feature_values = feature_instance.create_features(documents)
            msg = 'Successfully build {} for {} documents.'.format(feature_key, len(documents.all()))
            print(msg)
    
    def update_document_features(self, document, feature_key):
        feature_instance = self.features.get(feature_key, None)
        if feature_instance is not None:
            feature_instance.update_feature(document)
    
    def remove_document_features(self, documents, feature_key):
        feature_instance = self.features.get(feature_key, None)
        if feature_instance is not None:
            feature_instance.remove_features(documents)
