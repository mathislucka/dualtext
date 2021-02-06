from django.contrib.auth.models import User, Group
import factory
import factory.fuzzy
from dualtext_api.models import Annotation, Corpus, Document, Project, Task, Label

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    is_superuser = False
    password = factory.Faker('name')

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

class CorpusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Corpus

    name = factory.Faker('first_name')
    corpus_meta = {}

    @factory.post_generation
    def allowed_groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.allowed_groups.add(group)

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker('first_name')
    annotation_document_duplicates = True
    use_reviews = True
    annotation_mode = 'dualtext'

    @factory.post_generation
    def allowed_groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.allowed_groups.add(group)

    @factory.post_generation
    def corpora(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for corpus in extracted:
                self.corpora.add(corpus)

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Faker('first_name')
    project = factory.SubFactory(ProjectFactory)
    annotator = factory.SubFactory(UserFactory)
    is_finished = False
    copied_from = None
    action = 'annotate'


class AnnotationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Annotation
    task = factory.SubFactory(TaskFactory)
    is_finished = False
    copied_from = None
    action = 'annotate'

    @factory.post_generation
    def documents(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for document in extracted:
                self.documents.add(document)

    @factory.post_generation
    def labels(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for label in extracted:
                self.labels.add(label)

class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document

    content = factory.Faker('text')
    corpus = factory.SubFactory(CorpusFactory)

class LabelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Label

    name = factory.Faker('first_name')
    project = factory.SubFactory(ProjectFactory)
    color = {"standard": "#97C0E8", "light": "#EAF2FA"}
    key_code = factory.fuzzy.FuzzyChoice(['q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g'])
