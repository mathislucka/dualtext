from django.contrib.auth.models import User
from django.db.models import Q
from dualtext_api.models import Task, Annotation

class UserService():
    """
    A service to obtain data on users.
    """
    def __init__(self, user_id):
        self.user = User.objects.get(id=user_id)
        # Tasks
        self.user_tasks = None
        self.open_annotation_tasks = None
        self.closed_annotation_tasks = None
        self.open_review_tasks = None
        self.closed_review_tasks = None

        # Annotations
        self.closed_annotations = None
        self.open_annotations = None
        self.closed_reviews = None
        self.open_reviews = None
    
    def get_user_tasks(self):
        if self.user_tasks is not None:
            return self.user_tasks
        else:
            self.user_tasks = Task.objects.filter(annotator=self.user)
            return self.user_tasks

    def get_open_annotation_tasks(self):
        if self.open_annotation_tasks is not None:
            return self.open_annotation_tasks
        else:
            self.open_annotation_tasks = self.get_user_tasks().filter(
                Q(action__in=[Task.ANNOTATE, Task.DUPLICATE]) & Q(is_finished=False)
            )
            return self.open_annotation_tasks

    def get_open_review_tasks(self):
        if self.open_review_tasks is not None:
            return self.open_review_tasks
        else:
            self.open_review_tasks = self.get_user_tasks().filter(Q(action=Task.REVIEW) & Q(is_finished=False))
            return self.open_review_tasks

    def get_closed_annotation_tasks(self):
        if self.closed_annotation_tasks is not None:
            return self.closed_annotation_tasks
        else:
            self.closed_annotation_tasks = self.get_user_tasks().filter(
                Q(action__in=[Task.ANNOTATE, Task.DUPLICATE]) & Q(is_finished=True)
            )
            return self.closed_annotation_tasks

    def get_closed_review_tasks(self):
        if self.closed_review_tasks is not None:
            return self.closed_review_tasks
        else:
            self.closed_review_tasks = self.get_user_tasks().filter(Q(action=Task.REVIEW) & Q(is_finished=True))
            return self.closed_review_tasks

    def get_closed_annotations(self):
        if self.closed_annotations is not None:
            return self.closed_annotations
        else:
            self.closed_annotations = Annotation.objects.filter(task__in=self.get_closed_annotation_tasks())
            return self.closed_annotations

    def get_closed_reviews(self):
        if self.closed_reviews is not None:
            return self.closed_reviews
        else:
            self.closed_reviews = Annotation.objects.filter(task__in=self.get_closed_review_tasks())
            return self.closed_reviews

    def get_open_annotations(self):
        if self.open_annotations is not None:
            return self.open_annotations
        else:
            self.open_annotations = Annotation.objects.filter(task__in=self.get_open_annotation_tasks())
            return self.open_annotations

    def get_open_reviews(self):
        if self.open_reviews is not None:
            return self.open_reviews
        else:
            self.open_reviews = Annotation.objects.filter(task__in=self.get_open_review_tasks())
            return self.open_reviews

    def get_user_statistics(self):
        total_tasks = self.get_user_tasks().count()
        open_annotation_tasks = self.get_open_annotation_tasks().count()
        closed_annotation_tasks = self.get_closed_annotation_tasks().count()
        open_review_tasks = self.get_open_review_tasks().count()
        closed_review_tasks = self.get_closed_review_tasks().count()

        open_annotations = self.get_open_annotations().count()
        closed_annotations = self.get_closed_annotations().count()
        open_reviews = self.get_open_reviews().count()
        closed_reviews = self.get_closed_reviews().count()
        total_annotations = open_annotations + closed_annotations
        total_reviews = open_reviews + closed_reviews

        return {
            'tasks': {
                'total': total_tasks,
                'annotations': {
                    'open': open_annotation_tasks,
                    'closed': closed_annotation_tasks,
                },
                'reviews': {
                    'open': open_review_tasks,
                    'closed': closed_review_tasks,
                }
            },
            'annotations': {
                'annotator': {
                    'total': total_annotations,
                    'open': open_annotations,
                    'closed': closed_annotations,
                },
                'reviewer': {
                    'total': total_reviews,
                    'open': open_reviews,
                    'closed': closed_reviews,
                }
            }
        }