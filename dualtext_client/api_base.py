class ApiBase():
    """
    docstring
    """
    def __init__(self, session):
        self.base_url = 'http://localhost:8000/api/v1'
        self.session = session

    def get(self, resource_id):
        response = self.session.get(self.single_resource_path.format(resource_id))
        return self.process_response(response)

    def list_resources(self, params):
        response = self.session.get(self.list_resources_path, params=params)
        return self.process_response(response)

    def create(self, payload):
        response = self.session.post(self.list_resources_path, json=payload)
        return self.process_response(response)

    def update(self, payload):
        response = self.session.patch(self.single_resource_path.format(payload['id']), json=payload)
        return self.process_response(response)
    
    def delete(self, resource_id):
        response = self.session.delete(self.single_resource_path.format(resource_id))
        return self.process_response(response)

    def process_response(self, response):
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()
        return None

