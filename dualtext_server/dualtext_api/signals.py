from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Task, Document, Corpus
from dualtext_api.services import TaskService
from dualtext_api.haystack_documents import DualtextDocument

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
        # tasks that already have a review should not be reviewed again
        condition = bool(condition and task.task_set.filter(action=Task.REVIEW).count() == 0)
        if condition:
            ts = TaskService()
            ts.copy_task(task.id)


@receiver(post_save, sender=Document)
def generate_document_features_on_document_creation(sender, **kwargs):
    if kwargs['created']:
        document = kwargs['instance']
        document_update = Document.objects.get(id=document.id)
        dualtext_document = DualtextDocument(model_instance=document_update)
        dualtext_document.save()


@receiver(pre_delete, sender=Corpus)
def delete_document_features_on_corpus_deletion(sender, **kwargs):
    pass
    # TODO implement corpus deletion in haystack connector
    # corpus = kwargs['instance']
    # builder = Builder()
    # documents = corpus.document_set.all()
    # features = corpus.feature_set.all()
    #
    # for feature in features:
    #     builder.remove_document_features(documents, feature.key)
