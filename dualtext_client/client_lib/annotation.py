from .api_base import ApiBase

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

            if anno_labels:
                label_ids = [labels[label_name] for label_name in anno_labels]
                payload['labels'] = label_ids

            if doc_anno_lookup and doc_anno_lookup.get(anno['identifier'], None):
                payload['documents'] = doc_anno_lookup[anno['identifier']]

            if group_annotation_lookup and group_annotation_lookup.get(anno['identifier'], None):
                payload['annotation_group'] = group_annotation_lookup[anno['identifier']]

            created_annotations.append(self.create(payload))

        return created_annotations
