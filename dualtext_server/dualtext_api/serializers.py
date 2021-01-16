from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from dualtext_api.models import Annotation, Project, Corpus, Task, Document, Prediction, Label, Feature
from dualtext_api.services import ProjectService
from .validators import validate_alphabetic

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
        fields = ['id', 'name', 'allowed_groups', 'creator', 'corpora', 'task_set', 'annotation_mode'] + DEFAULT_FIELDS
        extra_kwargs = {
            'allowed_groups': {'required': False},
            'corpora': {'required': False},
            'task_set': {'required': False},
            'annotation_mode': {'required': False},
        }
        read_only_fields = ['creator']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'annotator',
            'is_finished',
            'action',
            'project'
        ] + DEFAULT_FIELDS
        extra_kwargs = {
            'is_finished': {'required': False},
            'action': {'required': False},
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
            'labels',
            'task',
            'prediction_set',
            'action',
            'copied_from'
        ] + DEFAULT_FIELDS
        extra_kwargs = {
            'labels': {'required': False},
            'prediction_set': {'required': False},
            'documents': {'required': False},
        }
        read_only_fields = ['task', 'action', 'copied_from']

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
            ),
            UniqueTogetherValidator(
                queryset=Label.objects.all(),
                fields=['key_code', 'project']
            ),
        ]
    def validate_key_code(self, value):
        return validate_alphabetic(value)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name', 'corpus', 'description', 'key'] + DEFAULT_FIELDS
        extra_kwargs = {
            'description': {'required': False},
        }