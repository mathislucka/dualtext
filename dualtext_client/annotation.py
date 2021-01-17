from api_base import ApiBase

class Annotation(ApiBase):
    """
    A class to interact with annotations from the dualtext api.
    """
    def __init__(self, session, task_id):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/annotation/{}'
        self.list_resources_path = self.base_url + '/task/{}/annotation/'.format(task_id)
        self.schema = 'annotation.schema.json'
