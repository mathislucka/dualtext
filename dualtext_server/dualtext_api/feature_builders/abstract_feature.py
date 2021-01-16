from abc import ABC, abstractmethod

class AbstractFeature(ABC):
    @abstractmethod
    def create_features(self, documents):
        """
        This method receives a list of documents for which it should create a feature.
        If necessary the saving of feature values to the DB is handled here.
        Features should be recreated from scratch.
        Any external feature representation (e.g. an ElasticSearch index) should be deleted and recreated.
        Deletion of stale feature values inside the DB is handled by the caller. 
        """
        pass
    @abstractmethod
    def update_feature(self, document):
        """
        This method receives a single document. It should update the single document's feature value.
        If necessary the saving of the updated feature value to the DB is handled here.
        Any external feature representation (e.g. ElasticSearch index) should be updated too.
        """
        pass

    @abstractmethod
    def remove_features(self, documents):
        """
        This method receives a list of documents. It should remove the feature values of these documents.
        If necessary the deletion of the feature value from the DB is handled here.
        Any external feature representation (e.g. ElasticSearch index) should be removed too.
        """
        pass

    @abstractmethod
    def process_query(self, query):
        """
        This method is needed if the feature is used in search and a query
        needs to be processed before being usable in search. It receives a string query and
        should return a featurized representation for that string (e.g. embedding it as a vector for sentence embedding search).
        """
        pass