from .api_base import ApiBase

class AnnotationGroup(ApiBase):
    """
    A class to interact with annotation groups from the dualtext api.
    """
    def __init__(self, session, task_id):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/annotation-group/{}'
        self.list_resources_path = self.base_url + '/task/{}/annotation-group/'.format(task_id)
        self.schema = 'annotation_group.schema.json'
