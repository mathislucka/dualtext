from django.db.models import Q
from operator import itemgetter
from dualtext_api.models import Project, Annotation

class ProjectService():
    def __init__(self, project_id):
        self.project = Project.objects.get(id=project_id)

    def get_total_annotations(self):
        tasks = [task.id for task in self.get_total_tasks().all()]
        return Annotation.objects.filter(task__id__in=tasks)

    def get_annotated_annotations(self):
        tasks = [task.id for task in self.get_total_tasks().all()]
        return Annotation.objects.filter(Q(task__in=tasks) & Q(task__is_annotated=True))

    def get_reviewed_annotations(self):
        tasks = [task.id for task in self.get_total_tasks().all()]
        return Annotation.objects.filter(Q(task__in=tasks) & Q(task__is_reviewed=True))

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
        return self.project.task_set.filter(is_annotated=True)

    def get_reviewed_tasks(self):
        return self.project.task_set.filter(is_reviewed=True)

    def get_total_tasks(self):
        return self.project.task_set
    
    def get_open_annotation_tasks(self):
        return self.project.task_set.filter(Q(is_annotated=False) & Q(annotator=None))
    
    def get_open_review_tasks(self):
        return self.project.task_set.filter(Q(is_annotated=True) & Q(is_reviewed=False) & Q(reviewer=None))
    
    def claim_annotation_task(self, user):
        task = self.get_open_annotation_tasks().first()
        if task is not None:
            task.annotator = user
            task.save()
            return task
        else:
            return None
    
    def claim_review_task(self, user):
        task = self.get_open_review_tasks().first()
        if task is not None:
            task.reviewer = user
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
        tasks = self.get_total_tasks().all()
        label_counts = {}

        for task in tasks:
            for label in labels:
                cnt = self.get_task_label_count(task, label)
                prev_count = label_counts.get(cnt[0], 0)
                label_counts[cnt[0]] = prev_count + cnt[1]

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

    def get_task_label_count(self, task, label):
        annotations = task.annotation_set.all()
        label_count = 0
        for annotation in annotations:
            labels = annotation.annotator_labels.all()
            reviewer = annotation.reviewer_labels.all()
            anno_count = len([l for l in labels if label.id == l.id and len(reviewer) == 0])
            rev_count = len([l for l in reviewer if l.id == label.id])
            label_count = label_count + anno_count + rev_count

        return (label.name, label_count)

    def get_project_statistics(self):
        return {
            'annotations': self.get_annotation_statistics(),
            'labels': self.get_label_statistics(),
            'tasks': self.get_task_statistics()
        }

    def get_desired_label(self):
        labelStatistics = self.get_label_statistics()['absolute']
        sortedStatistics = [(k, v) for k, v in labelStatistics.items()]
        sortedStatistics.sort(key=itemgetter(1))
        labelName = None
        if len(sortedStatistics) > 0:
            labelName = sortedStatistics[0][0]
        return labelName
        