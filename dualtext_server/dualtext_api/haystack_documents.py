from dualtext_api.haystack_connector.document import Document


class DualtextDocument(Document):
    fields = ['content', 'corpus__id', 'id']
    content_field = 'content'
    id_field = 'id'
    index_by = 'corpus__id'
    # indexing_pipelines = ['elastic_index']
    # query_pipelines = ['elastic_query', 'alternative_query']
