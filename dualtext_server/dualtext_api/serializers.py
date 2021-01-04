from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from dualtext_api.models import Annotation, Project, Corpus, Task, Document, Prediction, Label
from dualtext_api.services import ProjectService

DEFAULT_FIELDS = ['created_at', 'modified_at']

class CorpusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, validators=[
        UniqueValidator(queryset=Corpus.objects.all())
    ])
    class Meta:
        model = Corpus
        fields = ['id', 'name', 'corpus_meta', 'document_set'] + DEFAULT_FIELDS
        extra_kwargs = { 'document_set': {'required': False}}

class DocumentSerializer(serializers.ModelSerializer):
    method = serializers.CharField(read_only=True)
    class Meta:
        model = Document
        fields = ['id', 'content', 'corpus', 'method'] + DEFAULT_FIELDS
        read_only_fields = ['corpus']

class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, validators=[
        UniqueValidator(queryset=Project.objects.all())
    ])
    class Meta:
        model = Project
        fields = ['id', 'name', 'allowed_groups', 'creator', 'corpora', 'task_set'] + DEFAULT_FIELDS
        extra_kwargs = {
            'allowed_groups': {'required': False},
            'corpora': {'required': False},
            'task_set': {'required': False},
        }
        read_only_fields = ['creator']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'annotator',
            'reviewer',
            'is_annotated',
            'is_reviewed',
            'project'
        ] + DEFAULT_FIELDS
        extra_kwargs = {
            'is_annotated': {'required': False},
            'is_reviewed': {'required': False},
            'reviewer': {'required': False},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Task.objects.all(),
                fields=['name', 'project']
            )
        ]

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = [
            'id',
            'documents',
            'annotator_labels',
            'reviewer_labels',
            'task',
            'prediction_set',
            'is_reviewed'
        ] + DEFAULT_FIELDS
        extra_kwargs = {
            'reviewer_labels': {'required': False},
            'annotator_labels': {'required': False},
            'prediction_set': {'required': False},
            'documents': {'required': False},
            'is_reviewed': {'required': False},
        }
        read_only_fields = ['task']

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'annotation', 'score', 'method', 'label'] + DEFAULT_FIELDS

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'project', 'color', 'key_code'] + DEFAULT_FIELDS
        extra_kwargs = {
            'color': {'required': False},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Label.objects.all(),
                fields=['name', 'project']
            )
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
