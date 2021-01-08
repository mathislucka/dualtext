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

        feature_instance = self.features[feature_key]
        feature_values = feature_instance.process_documents(documents)

        feature = Feature.objects.get(key=feature_key)
        new_feature_values = []
        for val in feature_values:
            document_id = val[0]
            feature_value = val[1]
            fv = FeatureValue(value=feature_value, feature=feature)
            fv.document_id = document_id
            new_feature_values = new_feature_values + [fv]

        FeatureValue.objects.bulk_create(new_feature_values)
        msg = 'Successfully build {} for {} documents.'.format(feature_key, len(documents.all()))
        print(msg)
