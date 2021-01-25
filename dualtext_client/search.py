from api_base import ApiBase

class Search(ApiBase):
    """
    A class to retrieve documents via search from the dualtext API.
    """
    def __init__(self, session):
        super().__init__(session)
        self.single_resource_path = None
        self.list_resources_path = self.base_url + '/search/'
        self.schema = None

    def search(self, params, limit=None):
        response = self.session.get(self.list_resources_path, params=params)
        response = self.process_response(response)
        if limit is not None:
            response = response[:limit]
        return response
