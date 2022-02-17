import requests
import json


class IndexingPipeline:
    def __init__(self, pipeline_name, pipeline=None, url=None, token=None, batch_size=500):
        self.pipeline = pipeline

        self.url = url
        self.pipeline_name = pipeline_name
        self.token = token
        self.batch_size = batch_size

    def save(self, documents, index):
        if self.pipeline is None:
            self._make_indexing_request(documents, index)
        else:
            self.pipeline.run(documents=documents, params={'index': index})

    def _make_indexing_request(self, documents, index):
        for i in range(0, len(documents), self.batch_size):
            batch = documents[i:i+self.batch_size]
            body = {'documents': batch, 'params': {'index': index}}

            headers = {}
            if self.token is not None:
                headers = {'Authorization': f'Bearer {self.token}'}

            response = requests.post(self.url, json=json.dumps(body), headers=headers)
            response.raise_for_status()