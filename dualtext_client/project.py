from api_base import ApiBase
from annotation import Annotation
from corpus import Corpus
from document import Document
from label import Label
from task import Task
from feature import Feature
from label import Label

class Project(ApiBase):
    """
    A class to interact with projects from the dualtext api.
    """
    def __init__(self, session):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/project/{}'
        self.list_resources_path = self.base_url + '/project/'
        self.schema = 'project.schema.json'

    def create_from_scratch(self, data, task_size):
        self.validate_data(data, 'project_from_scratch.schema.json')
        corpus = Corpus(self.session)
        created_corpus = corpus.create(data['corpus'])
        features = data.get('features', None)
        if features is not None:
            self.add_corpus_features(created_corpus['id'], features)

        project_data = data['project']
        project_data['corpora'] = [ created_corpus['id'] ]
        project = self.create(project_data)

        labels = data.get('labels', None)
        if labels is not None:
            labels = self.create_labels(labels, project['id'])

        tasks = self.split_list(data['annotations'], task_size)

        for idx, task_chunk in enumerate(tasks):
            self.create_project_task(task_chunk, project['id'], idx, created_corpus['id'], labels)
        return project

    def create_annotation_documents(self, documents, corpus_id):
        doc = Document(self.session, corpus_id)
        document_ids = []
        for document in documents:
            created_document = doc.create({'content': document})
            document_ids.append(created_document['id'])
        return document_ids

    def split_list(self, lst, chunk_size):
        return [lst[i * chunk_size:(i + 1) * chunk_size] for i in range((len(lst) + chunk_size - 1) // chunk_size )]

    def create_project_task(self, task_chunk, project_id, task_idx, corpus_id, labels):
        task_instance = Task(self.session, project_id)
        task = task_instance.create({'name': 'P{}T{}'.format(project_id, task_idx)})
        self.create_annotations(task_chunk, labels, task['id'], corpus_id)

    def create_annotations(self, annotations, labels, task_id, corpus_id):
        annotation_instance = Annotation(self.session, task_id)
        for annotation in annotations:
            payload = {}

            documents = annotation.get('documents', None)
            if documents is not None:
                doc_ids = self.create_annotation_documents(annotation['documents'], corpus_id)
                payload['documents'] = doc_ids
            
            anno_labels = annotation.get('labels', None)
            if anno_labels is not None:
                label_ids = []
                for label in anno_labels:
                    label_ids.append(labels[label])
                payload['labels'] = label_ids

            annotation_instance.create(payload)

    def add_corpus_features(self, corpus_id, features):
        feature_instance = Feature(self.session)
        existing_features = feature_instance.list_resources()
        for feature in existing_features:
            if feature['key'] in features:
                feature['corpora'].append(corpus_id)
                feature_instance.update(feature)
    
    def create_labels(self, labels, project_id):
        label_instance = Label(self.session, project_id)
        created_labels = []
        for label in labels:
            l = label_instance.create(label)
            created_labels.append(l)
        return self.transform_labels(created_labels)

    def transform_labels(self, labels):
        transformed_labels = {}
        for label in labels:
            transformed_labels[label['name']] = label['id']
        return transformed_labels


