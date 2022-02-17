import itertools
from .pipeline_queryset import PipelineQueryset
from.pipelines import initialized_pipelines
from .custom_pipelines import document_store

indexing_pipelines = initialized_pipelines['indexing']

class Document:
    model = None
    fields = []
    content_field = None
    id_field = None
    indexing_pipelines = []
    query_pipelines = []
    current_fields = {}
    additional_fields = []
    index_by = 'class_name'

    def __init__(self, model_instance, **kwargs):
        for key, value in kwargs:
            self._check_and_set_arguments(kwargs, lookup=['additional_fields'])

        for field in self.fields:
            split_field = field.split('__')
            current_item = model_instance
            for attribute in split_field:
                current_item = getattr(current_item, attribute)

            self.current_fields[field] = current_item

        if self.index_by != 'class_name':
            attr_chain = self.index_by.split('__')
            resolved_attribute = model_instance
            for attr in attr_chain:
                resolved_attribute = getattr(resolved_attribute, attr)
            self.index = resolved_attribute
        else:
            self.index = self.__class__.__name__

        self.indexing_pipelines = {p_name: indexing_pipelines[p_name] for p_name in self.indexing_pipelines}

    def update(self, **kwargs):
        self._check_and_set_arguments(kwargs)

        return self

    def _check_and_set_arguments(self, arguments, lookup=None):
        if lookup is None:
            lookup = ['fields', 'additional_fields']

        check_fields = list(itertools.chain(*[self.__getattribute__(l) for l in lookup]))
        for key, value in arguments.items():
            if key not in check_fields:
                raise TypeError(
                    f'Unexpected keyword argument. Field {key} is not registered on {self.__class__.__name__}'
                )
            else:
                self.current_fields[key] = value

    def save(self):
        resource = {'meta': {}}
        resource['content'] = self.current_fields.get(self.content_field, None)
        resource['id'] = self.current_fields.get(self.id_field, None)

        for key, value in self.current_fields.items():
            if key != self.content_field:
                resource['meta'][key] = value

        for pipeline in self.indexing_pipelines:
            try:
                indexing_pipelines[pipeline].save([resource], self.index)
            except KeyError:
                raise ValueError(f'{pipeline} does not exist.')

    @classmethod
    def query_pipeline(cls, pipeline_name, index=None):
        query_index = index if index else cls.__class__.__name__
        if pipeline_name not in cls.query_pipelines:
            raise ValueError(f'{cls.__class__.__name__} does not have a "{pipeline_name}" query pipeline.')

        return PipelineQueryset(cls, pipeline_name, query_index)

    @classmethod
    def save_batch(cls, documents, index, common_attributes, unique_attributes=None):
        prepared_documents = [
            {'content': getattr(doc, cls.content_field), 'id': getattr(doc, cls.id_field), 'meta': {**common_attributes}}
            for doc in documents
        ]

        if unique_attributes is not None:
            for document, prepared_document in zip(documents, prepared_documents):
                for attribute in unique_attributes:
                    split_attribute = attribute.split('__')
                    current_item = document
                    for attr in split_attribute:
                        current_item = getattr(current_item, attr)

                    prepared_document[attribute] = current_item

        for pipeline in cls.indexing_pipelines:
            try:
                indexing_pipelines[pipeline].save(prepared_documents, index)
                docs = document_store.get_all_documents(index=index)
                print(docs)
            except KeyError:
                raise ValueError(f'{pipeline} does not exist.')

    def __repr__(self):
        return f'<{self.__class__.__name__}: {str(self.current_fields)}>'
