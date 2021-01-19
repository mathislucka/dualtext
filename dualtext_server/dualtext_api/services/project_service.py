from django.db.models import Q
from operator import itemgetter
from dualtext_api.models import Project, Annotation, Label, Task
from sklearn.metrics import confusion_matrix
import math

class ProjectService():
    def __init__(self, project_id):
        self.project = Project.objects.get(id=project_id)
        
        self.total_annotations = None
        self.annotated_annotations = None
        self.reviewed_annotations = None

        self.total_tasks = None
        self.annotated_tasks = None
        self.reviewed_tasks = None
        self.open_annotation_tasks = None
        self.open_review_tasks = None

    def get_total_annotations(self):
        if self.total_annotations is not None:
            return self.total_annotations
        else:
            tasks = self.get_total_tasks()
            self.total_annotations = Annotation.objects.filter(task__in=tasks.all())
            return self.total_annotations

    def get_annotated_annotations(self):
        if self.annotated_annotations is not None:
            return self.annotated_annotations
        else:
            tasks = self.get_total_tasks()
            annotations = self.get_total_annotations().filter(Q(task__is_finished=True) & Q(task__action__in=[Annotation.ANNOTATE, Annotation.DUPLICATE]))
            self.annotated_annotations = annotations
            return self.annotated_annotations

    def get_reviewed_annotations(self):
        if self.reviewed_annotations is not None:
            return self.reviewed_annotations
        else:
            tasks = self.get_total_tasks()
            annotations = self.get_total_annotations().filter(Q(task__is_finished=True) & Q(task__action=Task.REVIEW))
            self.reviewed_annotations = annotations
            return self.reviewed_annotations

    def get_annotation_statistics(self):
        total = self.get_total_annotations().count()
        annotated = self.get_annotated_annotations().count()
        reviewed = self.get_reviewed_annotations().count()

        if total != 0:
            percent_annotated = round(annotated / total, 2)
            percent_reviewed = round(reviewed / total, 2)
        else:
            percent_annotated = 0
            percent_reviewed = 0

        return {
            'total': total,
            'annotated_absolute': annotated,
            'annotated_relative': percent_annotated,
            'reviewed_absolute': reviewed,
            'reviewed_relative': percent_reviewed
        }

    def get_annotated_tasks(self):
        if self.annotated_tasks is not None:
            return self.annotated_tasks
        else:
            self.annotated_tasks = self.get_total_tasks().filter(Q(is_finished=True) & Q(action__in=[Task.ANNOTATE, Task.DUPLICATE]))
            return self.annotated_tasks

    def get_reviewed_tasks(self):
        if self.reviewed_tasks is not None:
            return self.reviewed_tasks
        else:
            self.reviewed_tasks = self.get_total_tasks().filter(Q(is_finished=True) & Q(action=Task.REVIEW))
            return self.reviewed_tasks

    def get_total_tasks(self):
        if self.total_tasks is not None:
            return self.total_tasks
        else:
            self.total_tasks = self.project.task_set
            return self.total_tasks
    
    def get_open_annotation_tasks(self, user):
        if self.open_annotation_tasks is not None:
            return self.open_annotation_tasks
        else:
            self.open_annotation_tasks = self.get_total_tasks().filter(
                Q(is_finished=False) &
                Q(action__in=[Task.ANNOTATE, Task.DUPLICATE]) &
                Q(annotator=None) &
                ~Q(copied_from__annotator=user)
            )
            return self.open_annotation_tasks
    
    def get_open_review_tasks(self, user):
        if self.open_review_tasks is not None:
            return self.open_review_tasks
        else:
            self.open_review_tasks = self.get_total_tasks().filter(
                Q(is_finished=False) &
                Q(action=Task.REVIEW) &
                Q(annotator=None) &
                ~Q(copied_from__annotator=user)
            )
            return self.open_review_tasks
    
    def claim_annotation_task(self, user):
        task = self.get_open_annotation_tasks(user).first()
        if task is not None:
            task.annotator = user
            task.save()
            return task
        else:
            return None
    
    def claim_review_task(self, user):
        task = self.get_open_review_tasks(user).first()
        if task is not None:
            task.annotator = user
            task.save()
            return task
        else:
            return None

    def get_task_statistics(self):
        total = self.get_total_tasks().count()
        annotated = self.get_annotated_tasks().count()
        reviewed = self.get_reviewed_tasks().count()
        if total != 0:
            percent_annotated = round(annotated / total, 2)
            percent_reviewed = round(reviewed / total, 2)
        else:
            percent_annotated = 0
            percent_reviewed = 0

        return {
            'total': total,
            'annotated_absolute': annotated,
            'annotated_relative': percent_annotated,
            'reviewed_absolute': reviewed,
            'reviewed_relative': percent_reviewed
        }

    def get_label_statistics(self):
        labels = self.project.label_set.all()
        label_counts = {}
        review_annotations = self.get_total_annotations().filter(action=Annotation.REVIEW).prefetch_related('labels')
        annotation_annotations = self.get_total_annotations().filter(Q(action=Annotation.ANNOTATE) & ~Q(annotation__in=review_annotations)).prefetch_related('labels')
        label_counts = {}

        for label in labels:
            label_counts[label.name] = 0
        
        for annotation in review_annotations:
            annotation_labels = annotation.labels.all()
            for label in annotation_labels:
                label_counts[label.name] += 1
        
        for annotation in annotation_annotations:
            annotation_labels = annotation.labels.all()
            for label in annotation_labels:
                label_counts[label.name] += 1

        total_labels = sum(label_counts.values())
        relative_label_counts = {}
        for item in label_counts.items():
            if total_labels != 0:
                rel = round(item[1] / total_labels, 2)
            else:
                rel = 0
            relative_label_counts[item[0]] = rel

        return {
            'absolute': label_counts,
            'relative': relative_label_counts,
            'total': total_labels
        }

    def get_project_statistics(self):
        return {
            'annotations': self.get_annotation_statistics(),
            'labels': self.get_label_statistics(),
            'tasks': self.get_task_statistics(),
            #'agreement': self.get_annotator_reviewer_agreement()
        }

    def get_desired_label(self):
        label_statistics = self.get_label_statistics()['absolute']
        sorted_statistics = [(k, v) for k, v in label_statistics.items()]
        sorted_statistics.sort(key=itemgetter(1))
        labels = None
        if len(sorted_statistics) > 0:
            label_count = Label.objects.filter(project=self.project).count()
            LOWER_THRESHOLD = 40
            label_num = math.floor(label_count/100 * LOWER_THRESHOLD)
            label_names = [ name for name, val in sorted_statistics[0:label_num]]
            labels = Label.objects.filter(name__in=label_names, project=self.project).all()
        return labels
    
    def get_annotator_reviewer_agreement(self):
        reviewed_annotations = self.get_reviewed_annotations()
        annotator_reviewer_matches = {}
        for annotation in reviewed_annotations:
            review_labels = [label.name for label in annotation.labels.all()]
            annotation_labels = [label.name for label in annotation.copied_from.labels.all()]
            for label in review_labels:
                if annotator_reviewer_matches.get(label, None) is None:
                    annotator_reviewer_matches[label] = {
                        'annotator': [],
                        'reviewer': []
                    }
                if label in annotation_labels:
                    annotator_reviewer_matches[label]['annotator'].append(label)
                    annotator_reviewer_matches[label]['reviewer'].append(label)
                else:
                    annotator_reviewer_matches[label]['annotator'].append('Not ' + label)
                    annotator_reviewer_matches[label]['reviewer'].append(label)
            for label in annotation_labels:
                if label in review_labels:
                    pass
                else:
                    if annotator_reviewer_matches.get(label, None) is None:
                        annotator_reviewer_matches[label] = {
                            'annotator': [],
                            'reviewer': []
                        }
                    annotator_reviewer_matches[label]['annotator'].append(label)
                    annotator_reviewer_matches[label]['reviewer'].append('Not ' + label)
        confusion = {}
        for label in annotator_reviewer_matches:
            matrix = confusion_matrix(annotator_reviewer_matches[label]['annotator'], annotator_reviewer_matches[label]['annotator'])
            confusion[label] = matrix
        return confusion
            






        