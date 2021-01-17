from api_base import ApiBase

class Task(ApiBase):
    """
    A class to interact with tasks from the dualtext api.
    """
    def __init__(self, session, project_id):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/task/{}'
        self.list_resources_path = self.base_url + '/project/{}/task/'.format(project_id)
        self.schema = 'task.schema.json'
