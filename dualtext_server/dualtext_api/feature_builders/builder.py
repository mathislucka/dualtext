from .sentence_embedding import SentenceEmbedding
from django.db.models import Q
from .sentence_farthest_neighbours import SentenceFarthestNeighbours
from ..models import Corpus, Document, FeatureValue, Feature

class Builder():
    def __init__(self):
        self.features = {'sentence_embedding': SentenceEmbedding(), 'sentence_farthest_neighbours': SentenceFarthestNeighbours()}

    def build_document_features(self, documents, feature_key):
        print('starting to build {} for {} documents...'.format(feature_key, len(documents.all())))
        stale_feature_values = FeatureValue.objects.filter(Q(document__in=documents) & Q(feature__key=feature_key)).delete()
        print('removed {} stale feature values'.format(stale_feature_values[0]))

        feature_instance = self.features.get(feature_key, None)
        if feature_instance is not None:
            feature_values = feature_instance.create_feature(documents)
            #self.save_features(feature_values, feature_key)
            msg = 'Successfully build {} for {} documents.'.format(feature_key, len(documents.all()))
            print(msg)
    
    def update_document_features(self, documents, feature_key):
        feature_instance = self.features.get(feature_key, None)
        if feature_instance is not None:
            feature_values = feature_instance.update_feature(documents)
            self.save_features(feature_values, feature_key)
    
    def save_features(self, feature_values, feature_key):
        feature = Feature.objects.get(key=feature_key)
        new_feature_values = []
        for val in feature_values:
            document_id = val[0]
            feature_value = val[1]
            fv = FeatureValue(value=feature_value, feature=feature)
            fv.document_id = document_id
            new_feature_values = new_feature_values + [fv]

        FeatureValue.objects.bulk_create(new_feature_values)

