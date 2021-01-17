from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Task, Document, Corpus
from dualtext_api.feature_builders.builder import Builder
from dualtext_api.services import TaskService

@receiver(pre_save, sender=Task)
def generate_review_on_task_completion(sender, instance, **kwargs):
    try:
        task = sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        pass
    else:
        # only tasks that change their completion state should generate reviews
        condition = task.is_finished != instance.is_finished
        # only completed tasks should generate reviews
        condition = bool(condition and instance.is_finished == True)
        # tasks that are copied from another task should not be reviewed another time
        condition = bool(condition and instance.copied_from == None)
        # reviews should only be generated if the project uses reviews
        condition = bool(condition and task.project.use_reviews == True)
        if condition:
            ts = TaskService()
            ts.copy_task(task.id)

@receiver(post_save, sender=Document)
def generate_document_features_on_document_creation(sender, **kwargs):
    if kwargs['created'] == True:
        document = kwargs['instance']
        builder = Builder()
        corpus = document.corpus
        features = corpus.feature_set.all()
        document_update = Document.objects.get(id=document.id)

        for feature in features:
            builder.update_document_features([document_update], feature.key)

@receiver(pre_delete, sender=Corpus)
def delete_document_features_on_corpus_deletion(sender, **kwargs):
    corpus = kwargs['instance']
    builder = Builder()
    documents = corpus.document_set.all()
    features = corpus.feature_set.all()

    for feature in features:
        builder.remove_document_features(documents, feature.key)
