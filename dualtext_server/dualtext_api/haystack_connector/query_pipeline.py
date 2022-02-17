import importlib
import requests
import json


class QueryPipeline:
    def __init__(self, pipeline_name, pipeline=None, url=None, token=None, batch_size=500, **kwargs):
        self.pipeline = pipeline
        self.url = url
        self.token = token
        self.batch_size = batch_size
        self.name = pipeline_name

        self.options = kwargs

    def search(self, query, filters, options):
        params ={'filters': filters, **options}
        if self.url is not None:
            response = self._perform_search_request(query, params)
        else:
            response = self.pipeline.run(query=query, params=params)

        return response

    def _perform_search_request(self, query, params):
        body = {'query': query, **params}
        headers = {}
        if self.token is not None:
            headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.post(self.url, json=json.dumps(body), headers=headers)
        response.raise_for_status()

        return response.json
