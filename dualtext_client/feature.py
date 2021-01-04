from api_base import ApiBase

class Feature(ApiBase):
    """
    A class to interact with features from the dualtext api.
    """
    def __init__(self, session, corpus_id):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/feature/{}'
        self.list_resources_path = self.base_url + '/corpus/{}/feature/'.format(corpus_id)
