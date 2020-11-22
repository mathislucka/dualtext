from django_elasticsearch_dsl import Document as ElasticDocument
from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.registries import registry
from .models import Document

@registry.register_document
class DocumentDocument(ElasticDocument):
    corpus = fields.NestedField(properties={
        'id': fields.IntegerField()
    })
    class Index:
        name = 'documents'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Document

        fields = ['content', 'id']
