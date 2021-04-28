from django.db.models import Q
from dualtext_api.models import Task, Annotation, AnnotationGroup

class TaskService():
    """
    A service to perform actions related to tasks.
    """
    def __init__(self):
        self.task_properties_to_copy = [
            ''
        ]

    def copy_task(self, task_id, action=Task.REVIEW):
        task = Task.objects.get(id=task_id)
        copies = task.task_set.all()
        name = task.name + action + str(len(copies))
        task_copy = Task(name=name, project=task.project, copied_from=task, action=action)
        task_copy.save()
        self.copy_task_annotations(task, task_copy, action)
        return Task.objects.get(id=task_copy.id)

    def copy_task_annotations(self, task, task_copy, action):
        annotations = task.annotation_set.all()
        group_group_copy_map = {}
        for annotation in annotations:
            annotation_copy = Annotation(task=task_copy, copied_from=annotation, action=action)
            if annotation.annotation_group:
                original_group_id = annotation.annotation_group.id
                group = group_group_copy_map.get(original_group_id, None)
                if group is None:
                    group = AnnotationGroup(task=task_copy)
                    group.save()
                    group_group_copy_map[original_group_id] = group
                annotation_copy.annotation_group = group

            annotation_copy.save()
            annotation_copy.documents.set(annotation.documents.all())
            annotation_copy.save()
