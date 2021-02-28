from abc import ABC, abstractmethod

class AbstractSearch(ABC):
    @abstractmethod
    def search(self, corpora, excluded_documents, query):
        """
        This method receives a list of corpora ids, ids of excluded documents and a query string.
        It searches the query string within the provided corpora (fetching the documents from the DB if necessary).
        It returns a sorted list of tuples. The tuples contain document id, search score and search method name.
        [(<id>, <score>, <method name>)]
        """
