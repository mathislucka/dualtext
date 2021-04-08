from .api_base import ApiBase

class Feature(ApiBase):
    """
    A class to interact with features from the dualtext api.
    """
    def __init__(self, session):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/feature/{}'
        self.list_resources_path = self.base_url + '/feature/'
