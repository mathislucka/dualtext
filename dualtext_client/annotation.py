from api_base import ApiBase

class Annotation(ApiBase):
    """
    A class to interact with annotations from the dualtext api.
    """
    def __init__(self, session, task_id):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/annotation/{}'
        self.list_resources_path = self.base_url + '/task/{}/annotation/'.format(task_id)
        self.schema = 'annotation.schema.json'

    def batch_create(self, annotations, labels=None, doc_anno_lookup=None, group_annotation_lookup=None):
        created_annotations = []
        for anno in annotations:
            payload = {}
            anno_labels = anno.get('labels', None)
            anno_meta = anno.get('annotation_meta', {})

            if anno_labels:
                label_ids = [labels[label_name] for label_name in anno_labels]
                payload['labels'] = label_ids

            payload['annotation_meta'] = anno_meta

            if doc_anno_lookup:
                meta_key = anno['identifier']['document_meta_key']
                anno_id = anno['identifier']['unique_id']
                documents = doc_anno_lookup
                annotation_documents = []
                for document in documents:
                    if anno_id in document['document_meta'][meta_key]:
                        annotation_documents.append(document)

                payload['documents'] = [None, None]

                for document in annotation_documents:
                    if document['document_meta']['doc_id'] == anno_id[:36]:
                        payload['documents'][0] = document['id']
                    else:
                        payload['documents'][1] = document['id']


            if group_annotation_lookup and group_annotation_lookup.get(anno['identifier'], None):
                payload['annotation_group'] = group_annotation_lookup[anno['identifier']]

            created_annotations.append(self.create(payload))

        return created_annotations
