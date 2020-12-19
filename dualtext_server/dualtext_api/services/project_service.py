from django.db.models import Q
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
            rel = round(item[1] / total_labels, 2)
            relative_label_counts[item[0]] = rel

        return {
            'absolute': label_counts,
            'relative': relative_label_counts,
            'total': total_labels
        }

    def get_task_label_count(self, task, label):
        label_count = task.annotation_set.filter(
            (Q(annotator_labels__id__contains=label.id) & Q(reviewer_labels=None)) | Q(reviewer_labels__id__contains=label.id)
        ).count()
        return (label.name, label_count)

    def get_project_statistics(self):
        return {
            'annotations': self.get_annotation_statistics(),
            'labels': self.get_label_statistics(),
            'tasks': self.get_task_statistics()
        }
        