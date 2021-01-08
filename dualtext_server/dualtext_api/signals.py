from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Task, Document
from dualtext_api.feature_builders.builder import Builder

# @receiver(pre_save, sender=Task)
# def generate_review_on_task_completion(sender, instance, **kwargs):
#     try:
#         task = sender.objects.get(id=instance.id)
#     except sender.DoesNotExist:
#         pass
#     else:
#         # only tasks that change their completion state should generate reviews
#         condition = task.is_finished != instance.is_finished
#         # only completed tasks should generate reviews
#         condition = condition & instance.is_finished == True
#         # tasks that are copied from another task should not be reviewed another time
#         condition = condition & instance.copied_from == None
#         # reviews should only be generated if the project uses reviews
#         condition = condition & task.project.use_reviews = True
#         if condition:
#             ts = TaskService()
#             ts.copy_task(task.id)

@receiver(post_save, sender=Document)
def generate_document_features_on_document_creation(sender, **kwargs):
    print(kwargs)
    if kwargs['created'] == True:
        document = kwargs['instance']
        builder = Builder()
        corpus = document.corpus
        features = corpus.feature_set.all()
        document_queryset = Document.objects.filter(id=document.id)

        for feature in features:
            print(feature)
            builder.build_document_features(document_queryset, feature.key)
    