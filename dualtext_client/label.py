from api_base import ApiBase

class Label(ApiBase):
    """
    A class to interact with labels from the dualtext api.
    """
    def __init__(self, session, project_id):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/label/{}'
        self.list_resources_path = self.base_url + '/project/{}/label'.format(project_id)
        self.schema = 'label.schema.json'
