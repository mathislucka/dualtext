**Please note that this project is under active development and is not yet stable. Use at your own discretion.**

# DUALTEXT
*unleash your annotation superpowers \o/*

Dualtext is an annotation tool for textual data specialized in sentence similarity annotations. Some of its features include:

- interactive annotation mode / find similar sentences through search using elasticsearch and BERT SentenceEmbeddings
- review and inter rater workflow / configure and automate creation of review and inter rater reliability tasks
- live statistics / always know the current state of your project, check progress, label distributions and timing estimations
- autobalanced datasets / balance your dataset by informing annotators about labels currently underrepresented
- API client / configure projects and corpora programatically
- CLI / create projects from the CLI

## Installation

Dualtext is a Django application using a Vue3 SPA-Frontend. Search functionality is provided through elasticsearch or custom search integrations.

**1. installing elasticsearch**

Dualtext uses elasticsearch. Go to: https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html and choose the appropriate installation method for your system.

Start elasticsearch: `$ sudo systemctl start elasticsearch.service` (more methods at https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html)

**2. get dualtext**

```bash
$ git clone git@github.com:mathislucka/dualtext.git
$ cd dualtext
```

Dualtext is split into 3 distinct modules. Under the root directory you will find:

`/dualtext_client` -> contains all API client and CLI related code

`/dualtext_server` -> contains all backend related code

`/frontend` -> contains all frontend related code

**3. getting the server running**

Go to `settings.py` in `dualtext_server/dualtext/` and point the `ELASTICSEARCH_DSL` entry to your elasticsearch host (default localhost:9200).
In `settings.py` configure the `DATABASES` according to your local DB setup. If you'd like to use SQLite:


```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Now create a virtual environment if you like.

Then:

```bash
$ pip install -r requirements.txt
$ cd dualtext_server
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py test
$ python manage.py runserver
```
Your server should now be running at `localhost:8000`. Note that a SentenceEmbedding model will be downloaded from the Huggingface model hub when you first run the tests or start the server. If you'd like to use a custom SentenceEmbedding model:

Go to `dualtext_server/dualtext_api/feature_builders/sentence_embedding.py:ln7` and change the model to a local file path or another SentenceEmbedding model from Huggingface.

**4. getting the frontend running**

Install node and npm (https://www.npmjs.com/get-npm).

Then go to `dualtext/frontend/` then:

```bash
$ npm install
$ npm run serve
```
Your local development server should now be running at `localhost:8080`. If you'd like to build your assets for production use `npm run build` instead.

**5. installing the CLI**

Go to `dualtext/dualtext_client/` then:

```bash
$ dualtext
```
You can now use the CLI.

## Guide

This aims to be a pragmatic guide to the most essential parts of dualtext. It covers working with the API from the CLI or the API client, using the dualtext frontend and implementing custom search methods or feature types in the dualtext backend.

### Using the API client and the CLI

Dualtext was built with automated management for annotation projects and corpora in mind.
The API client and the CLI enable developers and data scientists to interact with the API
from their own python programmes or from the command line. The focus of interacting with
the API lies in project and corpora management. You can create corpora, initiate projects
and download or discover data resulting from ongoing annotation. The full API schema can be
discovered at `<host>/api/v1/docs/` when the development server is running. It is served
in the form of a Swagger UI page informing the user on the basic structure of dualtext's API.
You can get a json representation of the schema at `<host>/openapi`.

To use the API client simply import the required modules from `dualtext_client/`. Each entity
that shall be used from the public API has a class containing all methods to interact with the
specific entity.

As an example, if you would like to create a corpus and corresponding documents you would do this:


```python
from dualtext_client.corpus import Corpus
from dualtext_client.session import Session
from dualtext_client.document import Document

# first establish a session
s = Session(username='your username', password='your password')

# Create a corpus instance using the established session
c = Corpus(session=s)

# now create a corpus
payload = {
    'name': '<name>', # a unique name for your corpus
    'corpus_meta': {}, # a json field accepting any meta information
    'allowed_groups': ['<int>', '<int>'], # a list of groups that shall be allowed to access the corpus
}
c = c.create(payload)

# now create some documents
# we are using the batch creation route which supports batches of up to 200 documents
d = Document(session=s, corpus=c.id)
documents = []
with open('some_file_path') as f:
        for line in f:
            documents.append({'content': line})
d.batch_create(documents)
```

You can find json schemas for most of these resources at `dualtext_client/schemas/`.

Using the CLI is a bit more simple. If you would like to create a new project from
a corpus of existing documents you would:

```bash
$ dualtext mkproj --project-data /some/file/path/file.json
```

The `mkproj` command accepts a file path to a json file containing all the information for your project as an argument.
You can find an example of the file's structure at `dualtext_client/examples/create_from_scratch/`.
The schema expected to be followed can be found at `dualtext_client/schemas/project_from_scratch.schema.json`.

### Implementing custom features and search methods

Dualtext is extensible. In its basic version it provides two search methods for searching inside corpora and one
feature that can be attached to each document in a corpus. A feature is a different representation of a document's
content. It can be a vector, a list of tokens, a tag or anything else that takes time to compute and that you
would like to permanently attach to a document. The basic concept is this:

A `Corpus` has one or more `Features` the feature contains a unique `feature_key`. The `feature_key` is used to retrieve
methods to build feature values from a feature builder class. As an example:

Corpus A has the feature `sentence_embedding`. A SentenceEmbedding class was created and the `sentence_embedding` key is
linked in the `Builder` class (`dualtext_server/dualtext_api/feature_builders/builder.py`). When a document is added to Corpus A
the corresponding sentence embedding is automatically computed according to the implementation inside the SentenceEmbedding class.

Let's build a custom feature to illustrate this:

```python
# /dualtext_server/dualtext_api/feature_builders/document_length.py
from .abstract_feature import AbstractFeature
from dualtext_api.models import Feature, FeatureValue, Document
import pickle

# all feature builders should inherit from abstract feature
# all necessary methods are documented in the AbstractFeature class
class DocumentLength(AbstractFeature):
    def create_feature(self, documents):
        # This method receives a list of documents
        feature = Feature.objects.get(key='document_length')

        for doc in documents:
            val = pickle.dumps(len(doc['content']))
            fv = FeatureValue(feature=feature, document=doc, value=val)
            fv.save()

    def update_features(self, documents):
        pass

    def remove_feature(self, documents):
        pass

    def process_query(self, query):
        return query
```

Now reference your newly build feature inside the Builder class:

```python
# /dualtext_server/dualtext_api/feature_builders/builder.py
# ...
from .document_length import DocumentLength

class Builder():
    def __init__(self):
        self.features = {'sentence_embedding': SentenceEmbedding(), 'elastic': Elastic(), 'document_length': DocumentLength()}
    # ...
```

Now you are done. When you assign a feature containing the feature key `document_length` to a corpus, the length of a document
will be automagically computed and saved alongside the document in your DB.

Let's build a custom search method that will retrieve all documents below a certain content length:

```python
# /dualtext_server/dualtext_api/search/document_length_search.py
from .abstract_search import AbstractSearch
import pickle

class DocumentLengthSearch(AbstractSearch):
    def __init__(self):
        self.feature_key = 'document_length'

    def search(self, corpora, excluded_documents, query):
        feature_values = FeatureValue.objects.filter(
            Q(key=self.feature_key) &
            Q(document__corpus__id__in=corpora) &
            ~Q(document__id__in=excluded_documents)
        ).all()

        found = []

        for fv in feature_values:
            length = pickle.loads(fv.value)
            if length < query:
                found.append((fv.document.id, length, self.feature_key))
        return found
```

`DocumentLengthSearch` inherits from `AbstractSearch` it has to implement a `search` method which will be run if the user decides to search for documents using their length. After implementing the custom search module, you need to reference the class in the global search class as follows:

```python
# /dualtext_server/dualtext_api/search.py
# ...
from .document_length_search import DocumentLengthSearch

class Search():
    # ...
    @staticmethod
    def get_available_methods():
        return {
            'elastic': ElasticSearch,
            'sentence_embedding': SentenceEmbeddingSearch,
            'document_length': DocumentLengthSearch
        }
```

The new search method can now be used.

In practice, you might not want to actually store feature values in the database and you might want to avoid using the DB for search requests in order to increase performance. You can look at feature and search implementations using elasticsearch in `/dualtext_server/dualtext_api/feature_builders/sentence_embedding.py` and `/dualtext_server/dualtext_api/search/sentence_embedding_search.py`.















