from django.db.models import Case, When, Q

from dualtext_api.models import Document, Project

class SearchService():
    """
    A class to perform actions related to searches.
    """
    def __init__(self, corpus_id, project_id=None):
        self.corpus_id = corpus_id
        self.project_id = project_id

    def postprocess_results(self, results, search_method):
        document_ids = []
        for document in results['documents']:
            if not isinstance(document, dict):
                document_ids.append(document.id)
            else:
                document_ids.append(document['id'])

        excluded_documents = self.get_excluded_documents()
        document_ids = [int(doc_id) for doc_id in document_ids if int(doc_id) not in excluded_documents]

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(document_ids)])
        queryset = Document.objects.filter(pk__in=document_ids).order_by(preserved)
        for idx, q in enumerate(queryset):
            q.method = search_method

        return queryset

    def get_excluded_documents(self):
        project = None
        excluded_documents = []
        if self.project_id:
            project = Project.objects.get(id=self.project_id)

        if project and project.annotation_document_duplicates == False:
            annotated_documents = Document.objects.filter(
                Q(corpus__id=self.corpus_id) & Q(annotation__task__project=project)
            )
            excluded_documents = list(annotated_documents.values_list('id', flat=True))
        print('excluded documents: {}'.format(excluded_documents))

        return excluded_documents
