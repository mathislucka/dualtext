from django.contrib.auth.models import User, Group
from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from dualtext_api.models import Annotation, Project, Corpus, Task, Document, Prediction, Label, Feature
from dualtext_api.models import AnnotationGroup
from .validators import validate_alphabetic
from .features import FeatureRunner
from django.utils import timezone

DEFAULT_FIELDS = ['created_at', 'modified_at']

class CorpusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, validators=[
        UniqueValidator(queryset=Corpus.objects.all())
    ])
    document_count = serializers.SerializerMethodField('count_documents')

    def count_documents(self, obj):
        try:
            return obj.document__count
        except AttributeError:
            return 0

    class Meta:
        model = Corpus
        fields = ['id', 'name', 'corpus_meta', 'document_count'] + DEFAULT_FIELDS
        extra_kwargs = { 'document_set': {'required': False}}
        read_only_fields = ['document_count']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class DocumentListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        documents = [Document(**item) for item in validated_data]
        now = timezone.now()
        Document.objects.bulk_create(documents)
        feature_runner = FeatureRunner()
        # This might be almost save to get an id from documents created in bulk_create
        # It is not impossible for another document to have been created by another process
        # since now was calculated but it's extremely unlikely that it has the same content.
        # Postgres apparently provides ids on bulk_create so this might be resolved later.
        contents = [doc.content for doc in documents]
        documents = Document.objects.filter(Q(created_at__gte=now) & Q(content__in=contents))
        if len(documents) > 0:
            corpus_id = documents[0].corpus.id
            feature_runner.update_features(documents, corpus_id)
        return documents

class DocumentSerializer(serializers.ModelSerializer):
    method = serializers.CharField(read_only=True)
    class Meta:
        list_serializer_class = DocumentListSerializer
        model = Document
        fields = ['id', 'content', 'corpus', 'method'] + DEFAULT_FIELDS
        read_only_fields = ['corpus', 'method']

class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, validators=[
        UniqueValidator(queryset=Project.objects.all())
    ])
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'allowed_groups',
            'creator',
            'corpora',
            'annotation_mode',
            'max_documents'
        ] + DEFAULT_FIELDS
        extra_kwargs = {
            'allowed_groups': {'required': False},
            'corpora': {'required': False},
            'annotation_mode': {'required': False},
            'max_documents': {'required': False},
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
            'project',
            'annotationgroup_set',
        ] + DEFAULT_FIELDS
        extra_kwargs = {
            'is_finished': {'required': False},
            'action': {'required': False},
        }
        read_only_fields = ['annotationgroup_set']

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
            'action',
            'copied_from',
            'annotation_group'
        ] + DEFAULT_FIELDS
        extra_kwargs = {
            'labels': {'required': False},
            'documents': {'required': False},
        }
        read_only_fields = ['action', 'copied_from']

    def validate(self, data):
        """
        Check that annotation and annotation_group belong to the same task.
        Check that annotations do not have more documents than the project allows.
        """
        group = data.get('annotation_group', None)
        task = data.get('task', None)

        if group and task and group.task.id != task.id:
            raise serializers.ValidationError("Annotation must belong to the same task as its group.")

        documents = data.get('documents', None)
        if task and documents:
            project = task.project
            max_documents = project.max_documents
            if len(documents) > max_documents:
                raise serializers.ValidationError(f'The annotation may have a maximum of {max_documents} documents.')

        return data

class AnnotationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationGroup
        fields = ['id', 'task'] + DEFAULT_FIELDS
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
        fields = ['id', 'name', 'corpora', 'description', 'key'] + DEFAULT_FIELDS
        extra_kwargs = {
            'description': {'required': False},
            'corpora': {'required': False},
        }