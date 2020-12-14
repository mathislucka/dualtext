from dualtext_api.models import Project

class ProjectService():
    def __init__(self, project_id):
        self.project = Project.objects.get(id=project_id)

    def get_annotated_tasks(self):
        return self.project.task_set.filter(is_annotated=True).count()

    def get_reviewed_tasks(self):
        return self.project.task_set.filter(is_reviewed=True).count()

    def get_annotation_count(self):
        pass