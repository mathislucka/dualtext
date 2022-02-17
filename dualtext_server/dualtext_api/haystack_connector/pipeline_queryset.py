from .pipelines import initialized_pipelines

query_pipelines = initialized_pipelines['query']

class PipelineQueryset:
    filters = {}
    options = {}
    query = ''

    def __init__(self, document_class, pipeline_name, index):
        try:
            self.pipeline = query_pipelines[pipeline_name]
        except KeyError:
            raise ValueError(f'{pipeline_name} does not exist.')

        self.document_class = document_class
        self.options['index'] = index

    def set_options(self, **kwargs):
        for key, value in kwargs.items():
            self.options[key] = value
        return self

    def filter(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.document_class.fields:
                raise TypeError(
                    f'Unexpected keyword argument. '
                    f'Document {self.document_class.__class__.__name__} does not have a {key} field.'
                )

            self.filters[key] = value

        return self

    def query(self, query):
        if not isinstance(query, str):
            raise TypeError(f'query needs to be of type string.')

        self.query = query

        return self

    def run(self):
        return self.pipeline.search(
            query=self.query,
            filters=self.filters,
            options=self.options
        )