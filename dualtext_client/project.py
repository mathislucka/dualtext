from api_base import ApiBase
from annotation import Annotation
from corpus import Corpus
from document import Document
from label import Label
from task import Task
from feature import Feature

class Project(ApiBase):
    """
    A class to interact with projects from the dualtext api.
    """
    def __init__(self, session):
        super().__init__(session)
        self.single_resource_path = self.base_url + '/project/{}'
        self.list_resources_path = self.base_url + '/project/'

    def create_from_scratch(self, data, task_size):
        corpus = Corpus(self.session)
        created_corpus = corpus.create(data['corpus'])
        features = data.get('features', None)
        if features is not None:
            self.create_corpus_features(created_corpus['id'], features)
        project_data = data['project']
        project_data['corpora'] = [ created_corpus['id'] ]
        project = self.create(project_data)

        tasks = self.split_list(data['annotations'], task_size)

        for idx, task_chunk in enumerate(tasks):
            self.create_project_task(task_chunk, project['id'], idx, created_corpus['id'])
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

    def create_project_task(self, task_chunk, project_id, task_idx, corpus_id):
        task_instance = Task(self.session, project_id)
        task = task_instance.create({'name': 'P{}T{}'.format(project_id, task_idx)})
        annotation_instance = Annotation(self.session, task['id'])
        for annotation in task_chunk:
            doc_ids = self.create_annotation_documents(annotation['documents'], corpus_id)
            annotation_instance.create({'documents': doc_ids})
    
    def create_corpus_features(self, corpus_id, features):
        feature_instance = Feature(self.session, corpus_id)
        for feature in features:
            feature['corpus'] = corpus_id
            feature_instance.create(feature)


