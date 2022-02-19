# from haystack.nodes import ElasticsearchRetriever
# from haystack.document_stores import ElasticsearchDocumentStore
# from haystack.pipelines import Pipeline
#
# class MockPipeline:
#     def run(self, **kwargs):
#         for key, value in kwargs.items():
#             print(key, value)
#
# document_store = ElasticsearchDocumentStore(
#     host="localhost",
#     username="",
#     password="",
#     embedding_field="emb",
#     embedding_dim=768,
#     excluded_meta_data=["emb"],
#     analyzer='german',
#     similarity='cosine'
# )
#
# retriever = ElasticsearchRetriever(document_store=document_store)
#
# elastic_index = Pipeline()
# elastic_index.add_node(document_store, 'ElasticSearch', inputs=['File'])
#
# elastic_query = Pipeline()
# elastic_query.add_node(retriever, 'ElasticRetriever', inputs=['Query'])
#
# alternative_query = Pipeline()
# alternative_query.add_node(retriever, 'ElasticRetriever', inputs=['Query'])
#
