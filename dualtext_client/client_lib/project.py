from .api_base import ApiBase
from .annotation import Annotation
from .corpus import Corpus
from .document import Document
from .label import Label
from .task import Task
from .feature import Feature
from .search import Search
from .annotation_group import AnnotationGroup
import math

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
        documents = data.get('documents', None)
        created_documents = None
        if documents is not None:
            created_documents = self.create_documents(documents, created_corpus['id'])

        groups = data.get('annotation_groups', None)
        if groups:
            groups = self.split_list(groups, task_size)
            for idx, chunk in enumerate(groups):
                annotation_ids = set()
                for group in chunk:
                    if group.get('annotation_ids', None):
                        annotation_ids.update(group['annotation_ids'])
                annotations = [anno for anno in data['annotations'] if anno['identifier'] in annotation_ids]
                self.create_project_task(annotations, project['id'], idx, labels, created_documents, chunk)
        else:
            annotations = self.split_list(data['annotations'], task_size)
            for idx, chunk in enumerate(annotations):
                self.create_project_task(chunk, project['id'], idx, labels, created_documents)

        return project

    def create_documents(self, documents, corpus_id):
        document_instance = Document(self.session, corpus_id)
        document_chunks = self.split_list(documents, 200)
        created_documents = {}
        for chunk in document_chunks:
            documents_to_create = []
            identifiers = []
            for doc in chunk:
                identifiers.append(doc.get('annotation_identifier', None))
                documents_to_create.append({'content': doc['content']})
            docs = document_instance.batch_create(documents_to_create)
            for idx, doc in enumerate(docs):
                _id = identifiers[idx]
                if _id is not None:
                    related_documents = created_documents.get(_id, [])
                    related_documents.append(doc['id'])
                    created_documents[_id] = related_documents
        return created_documents

    def split_list(self, lst, chunk_size):
        return [lst[i * chunk_size:(i + 1) * chunk_size] for i in range((len(lst) + chunk_size - 1) // chunk_size )]

    def create_project_task(self, annotations, project_id, task_idx=None, labels=None, documents=None, groups=None):
        task_instance = Task(self.session, project_id)
        task = task_instance.create({'name': 'P{}T{}'.format(project_id, task_idx)})
        annotation_group_lookup = None
        if groups is not None:
            annotation_group_lookup = self.create_groups(task, groups)
        return self.create_annotations(
            annotations=annotations,
            labels=labels,
            task_id=task['id'],
            documents=documents,
            annotation_group_map=annotation_group_lookup
        )

    def create_groups(self, task, groups):
        ag_instance = AnnotationGroup(self.session, task['id'])
        annotation_group_map = {}
        for group in groups:
            g = ag_instance.create({})
            for anno in group['annotation_ids']:
                annotation_group_map[anno] = g['id']
        return annotation_group_map

    def create_annotations(self, annotations, labels, task_id, documents, annotation_group_map):
        annotation_instance = Annotation(self.session, task_id)
        return annotation_instance.batch_create(
            annotations=annotations,
            labels=labels,
            doc_anno_lookup=documents,
            group_annotation_lookup=annotation_group_map
        )

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

    def create_from_documents(self, data, task_size):
        self.validate_data(data, 'project_from_documents.schema.json')
        project = self.create(data['project'])
        self.create_labels(data['labels'], project['id'])

        query = {
            'method': data['search_methods'],
            'corpus': project['corpora']
        }
        global_limit = data['limit']

        annotations_to_create = []
        s = Search(self.session)

        for doc in data['documents']:
            limit = math.floor(global_limit * doc['weight'])
            candidates = s.search(params={**query, 'query': doc['content']}, limit=limit)
            annotations_to_create.extend(candidates)

        chunks = self.split_list(annotations_to_create, task_size)
        project_id = project['id']
        task_instance = Task(self.session, project_id)
        for idx, chunk in enumerate(chunks):
            task = task_instance.create({'name': 'P{}T{}'.format(project_id, idx)})
            self.create_annotations_directly(task['id'], chunk)

        return project

    def create_annotations_directly(self, task_id, documents):
        annotation_instance = Annotation(self.session, task_id)
        for doc in documents:
            payload = {'documents': [doc['id']]}
            annotation_instance.create(payload)

    def get_annotations(self, project_id, task_params={}, annotation_params={}):
        self.validate_data(task_params, 'task_filter.schema.json')
        self.validate_data(annotation_params, 'annotation_filter.schema.json')
        task_instance = Task(self.session, project_id)
        label_instance = Label(self.session, project_id)
        labels = label_instance.list_resources()
        document_instance = Document(self.session)
        tasks = task_instance.list_resources(task_params)
        annotations = []
        doc_ids = []
        documents = []
        for task in tasks:
            anno_instance = Annotation(self.session, task['id'])
            annos = anno_instance.list_resources(annotation_params)
            for anno in annos:
                doc_ids += anno['documents']
            annotations.extend(annos)
        for doc_id in doc_ids:
            documents.append(document_instance.get(doc_id))
        return {
            'annotations': annotations,
            'documents': documents,
            'labels': labels
        }
