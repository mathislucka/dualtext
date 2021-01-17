import jsonschema
import os
import json
import pathlib
from requests.exceptions import HTTPError

class ApiBase():
    """
    docstring
    """
    def __init__(self, session):
        self.base_url = 'http://localhost:8000/api/v1'
        self.session = session
        self.absolute_path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'schemas')
        self.schema = None

    def get(self, resource_id):
        response = self.session.get(self.single_resource_path.format(resource_id))
        return self.process_response(response)

    def list_resources(self, params={}):
        response = self.session.get(self.list_resources_path, params=params)
        return self.process_response(response)

    def create(self, payload):
        self.validate_data(payload)
        response = self.session.post(self.list_resources_path, json=payload)
        return self.process_response(response)

    def update(self, payload):
        response = self.session.patch(self.single_resource_path.format(payload['id']), json=payload)
        return self.process_response(response)
    
    def delete(self, resource_id):
        response = self.session.delete(self.single_resource_path.format(resource_id))
        return self.process_response(response)

    def process_response(self, response):
        self.raise_for_errors(response)
        if response.status_code != 204:
            return response.json()
        return None

    def validate_data(self, data, schema_file=None):
        print(self.absolute_path)
        if schema_file == None:
            schema_file = self.schema
        if schema_file is not None:
            with open(os.path.join(self.absolute_path, schema_file)) as file_object:
                schema = json.load(file_object)
                resolver = jsonschema.RefResolver('file://' + self.absolute_path + '/', schema_file)
                jsonschema.Draft7Validator(schema, resolver=resolver).validate(data)

    def raise_for_errors(self, response):
        try:
            response.raise_for_status()
        except HTTPError as e:
            if 500 <= response.status_code < 600 or 404 == response.status_code:
                http_error_msg = u'%s Server Error: %s for url: %s' % (response.status_code, response.reason, response.url)
            elif 400 <= response.status_code < 500:
                http_error_msg = u'%s Client Error: %s for url: %s' % (response.status_code, response.json(), response.url)
            
            if http_error_msg:
                raise HTTPError(http_error_msg, response=response)
            else:
                raise e
        return


