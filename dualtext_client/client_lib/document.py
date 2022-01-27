from api_base import ApiBase

class Document(ApiBase):
    """
    A class to interact with documents from the dualtext api.
    """
    def __init__(self, session, corpus_id=None):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/document/{}'
        self.list_resources_path = self.base_url + '/corpus/{}/document/'.format(corpus_id)
        self.batch_path = self.base_url + '/corpus/{}/document/batch/'.format(corpus_id)
        self.schema = 'document.schema.json'

    def batch_create(self, documents):
        response = self.session.post(self.batch_path, json=documents)
        return self.process_response(response)
