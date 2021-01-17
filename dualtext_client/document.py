from api_base import ApiBase

class Document(ApiBase):
    """
    A class to interact with documents from the dualtext api.
    """
    def __init__(self, session, corpus_id):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/document/{}'
        self.list_resources_path = self.base_url + '/corpus/{}/document/'.format(corpus_id)
        self.schema = 'document.schema.json'
