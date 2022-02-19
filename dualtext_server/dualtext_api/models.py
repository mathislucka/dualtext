from django.db import models
from django.contrib.auth.models import User, Group
from .validators import validate_alphabetic

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
    DUALTEXT = 'dualtext'
    CLASSIFICATION = 'classification'
    GROUPED = 'grouped'
    MODE_CHOICES = (
        (DUALTEXT, 'dualtext'),
        (CLASSIFICATION, 'classification'),
        (GROUPED, 'grouped'),
    )
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_creator', null=True)
    corpora = models.ManyToManyField(Corpus)
    allowed_groups = models.ManyToManyField(Group, related_name='%(class)s_allowed')
    annotation_document_duplicates = models.BooleanField(blank=True, default=True)
    use_reviews = models.BooleanField(blank=True, default=True)
    annotation_mode = models.CharField(max_length=15, choices=MODE_CHOICES, blank=True, default=DUALTEXT)
    max_documents = models.IntegerField(blank=True, default=2)

    class Meta(AbstractBase.Meta):
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_project_name')
        ]


class Label(AbstractBase):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    color = models.JSONField()
    key_code = models.CharField(max_length=1, null=True, validators=[validate_alphabetic])

    class Meta(AbstractBase.Meta):
        constraints = [
            models.UniqueConstraint(fields=['name', 'project'], name='unique_label_name_in_project'),
            models.UniqueConstraint(fields=['key_code', 'project'], name='unique_key_code_in_project'),
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


class AnnotationGroup(AbstractBase):
    """
    An entity grouping annotations for more advanced annotation modes
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


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
    annotation_group = models.ForeignKey(AnnotationGroup, on_delete=models.CASCADE, null=True)


class Prediction(AbstractBase):
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    score = models.FloatField(null=True)
    method = models.CharField(max_length=255)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)


class Run(AbstractBase):
    """
    An entity measuring the time spent on a single annotation run.
    """
    is_finished = models.BooleanField(blank=True, default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time_to_completion = models.IntegerField(null=True)


class Lap(AbstractBase):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
