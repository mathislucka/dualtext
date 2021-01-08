from django.db import models
from django.contrib.auth.models import User, Group

class AbstractBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('created_at',)

class Corpus(AbstractBase):
    name = models.CharField(max_length=255)
    corpus_meta = models.JSONField()
    allowed_groups = models.ManyToManyField(Group)

    class Meta(AbstractBase.Meta):
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_corpus_name')
        ]

class Document(AbstractBase):
    content = models.TextField(blank=True, default='')
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE)

class Project(AbstractBase):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_creator', null=True)
    corpora = models.ManyToManyField(Corpus)
    allowed_groups = models.ManyToManyField(Group, related_name='%(class)s_allowed')
    annotation_document_duplicates = models.BooleanField(blank=True, default=True)
    use_reviews = models.BooleanField(blank=True, default=True)

    class Meta(AbstractBase.Meta):
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_project_name')
        ]

class Label(AbstractBase):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    color = models.JSONField()
    key_code = models.CharField(max_length=1, null=True)

    class Meta(AbstractBase.Meta):
        constraints = [
            models.UniqueConstraint(fields=['name', 'project'], name='unique_label_name_in_project')
        ]

class Task(AbstractBase):
    ANNOTATE = 'annotate'
    REVIEW = 'review'
    DUPLICATE = 'duplicate'
    ACTION_CHOICES = (
        (ANNOTATE, 'annotate'),
        (REVIEW, 'review'),
        (DUPLICATE, 'duplicate'),
    )
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_annotator', null=True)
    is_finished = models.BooleanField(blank=True, default=False)
    copied_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, blank=True, default=ANNOTATE)

    class Meta(AbstractBase.Meta):
        constraints = [
            models.UniqueConstraint(fields=['name', 'project'], name='unique_task_name_in_project')
        ]

class Annotation(AbstractBase):
    ANNOTATE = 'annotate'
    REVIEW = 'review'
    DUPLICATE = 'duplicate'
    ACTION_CHOICES = (
        (ANNOTATE, 'annotate'),
        (REVIEW, 'review'),
        (DUPLICATE, 'duplicate'),
    )
    documents = models.ManyToManyField(Document, blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_finished = models.BooleanField(blank=True, default=False)
    copied_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, blank=True, default=ANNOTATE)

class Prediction(AbstractBase):
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    score = models.FloatField(null=True)
    method = models.CharField(max_length=255)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

class Feature(AbstractBase):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default='')
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)

    class Meta(AbstractBase.Meta):
        constraints = [
            models.UniqueConstraint(fields=['key'], name='unique_feature_key'),
            models.UniqueConstraint(fields=['name'], name='unique_feature_name'),
        ]

class FeatureValue(AbstractBase):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    value = models.BinaryField()
