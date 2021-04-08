from .api_base import ApiBase

class Corpus(ApiBase):
    """
    A class to interact with corpora from the dualtext api.
    """
    def __init__(self, session):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/corpus/{}'
        self.list_resources_path = self.base_url + '/corpus/'
        self.schema = 'corpus.schema.json'
