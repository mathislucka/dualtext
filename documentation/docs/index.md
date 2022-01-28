# What is dualtext?

dualtext is a text annotation tool that can be used to create training data for machine learning models. dualtext is especially suited for the annotation of textual similarity data. If you want to match some documents with other documents from a text corpus, dualtext is the right tool for the job.

## Core features

- single label and multi label text classification
- multi-document text classification
- grouped annotation mode (i.e. for NLI annotations)
- find the right document matching your labels in interactive search mode
- create projects and download annotation data from the CLI
- self-service annotator task assignment
- integrated annotation review workflow
- live project statistics with time tracking
- manage your text corpora and use them for multiple annotation projects


# Installation and Setup

dualtext is a Django API-Backend using a Vue3 SPA-Frontend. Search functionality is provided through elasticsearch or custom search integrations. You will need to install multiple components to get dualtext up and running. This is a step-by-step explanation for the installation process. 

## Prerequisites

You will need the following software to install and run dualtext:

- python 3.8 (including pip) or higher -> follow installation instructions at https://wiki.python.org/moin/BeginnersGuide/Download
- Node.js (including npm) -> follow instructions at https://nodejs.org/en/download/
- Elasticsearch 7.13 or higher -> follow instructions at https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html

## Install dualtext

### 1. Get dualtext
```
$ git clone git@github.com:mathislucka/dualtext.git
$ cd dualtext
```

You will find the following directory structure:

```
dualtext
├─ documentation
├─ dualtext_client
├─ dualtext_server
├─ frontend
├─ .gitignore
├─ README.md
├─ requirements.txt
```

All code connected to the API-Backend can be found in `dualtext_server`. Code for the Vue3 SPA-Frontend can be found in `frontend`.

If you want to use the client lib or the CLI you will find relevant code in `dualtext_client`.

### 2. Configure dualtext

You will need to change some settings before being able to run the dualtext server:

```
dualtext$ cd dualtext_server/dualtext
dualtext/dualtext_server/dualtext$ cp settings.example.py settings.py
```
Now open up `settings.py` and add the following settings:

1. point the `ELASTICSEARCH_DSL` entry to your elasticsearch host (default localhost:9200)
2. configure `DATABASES` according to your local DB setup (sqlite below)
 ```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 3. Install dependencies

You will now need to install some python dependencies for dualtext:

```
dualtext$ pip install -r requirements.txt
```

### 4. Run database migrations

If you are installing dualtext for the first time or you are using a fresh database, you will need to create and run migrations for your database:

```
dualtext/dualtext_server$ python manage.py makemigrations
dualtext/dualtext_server$ python manage.py migrate
```

### 5. Create admin user

You will need to create a superuser if you are installing dualtext for the first time or you are using a fresh database.
You can find detailed information on django and django admin in the django documentation: https://docs.djangoproject.com/en/3.2/intro/tutorial02/#introducing-the-django-admin

For dualtext, the following command should suffice:

```
dualtext/dualtext_server$ python manage.py createsuperuser
```

### 6. Test and run the API-Backend

You should now be ready to start the dualtext server for the first time. Make sure you have started your elasticsearch cluster and changed the settings to point to your elasticsearch instance, then:

```
dualtext/dualtext_server$ python manage.py test
.
.
.
----------------------------------------------------------------------
Ran 120 tests in 3.617s

OK
Destroying test database for alias 'default'...

dualtext/dualtext_server$ python manage.py runserver
.
.
.
Django version 3.1.3, using settings 'dualtext.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

...
```

All tests should have passed and the API should now be running at `localhost:8000/`. You can verify that it is running properly by navigating to `localhost:8000/api/v1/docs/`. This should bring up the auto-generated API docs for the dualtext API-backend.

:::warning
This runs the Django development server. The development server is not suited for production.
See Django's deployment guide for more information on how to setup a Django project for production:
https://docs.djangoproject.com/en/3.2/howto/deployment/
:::


### 7. Verify CLI installation

dualtext comes with a command line interface (CLI) which can be used to create new annotation projects or to download data from existing projects. To verify that the dualtext CLI was installed properly, open up a terminal and check the installation:

```bash
dualtext$ dualtext
Usage: dualtext [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dlproj
  mkproj
```

If you get a `dualtext: Command not found` instead, the installation of the dualtext CLI was unsuccessful. 


### 8. Install frontend dependencies

To run the SPA-frontend you will need to install some dependencies first:

```
dualtext/frontend$ npm install
```

### 9. Run frontend app
Running the frontend for development purposes is as easy as:

```
dualtext/frontend$ npm run serve
```

The frontend should now be available at `localhost:8080`. If you navigate there, you should be prompted with a log-in screen. You can use the user name and password generated in step 5 to sign in.

:::warning
This runs the frontend in development mode. Refer to https://cli.vuejs.org/guide/deployment.html#general-guidelines to see how to deploy the frontend for production.
:::


# Core concepts

When annotating data for semantic textual similarity tasks, you usually try to match one document with other documents and depending on the annotation scheme you will also assign a label to the relationship between those documents.

For example, the Semantic Textual Similarity Benchmark (STS-B) uses an annotation scheme where two sentences are matched up and a label between 0 (not at all similar) and 5 (both sentences have the same meaning) is assigned. When annotating new datasets in a similar style, it is very challenging to present the annotator with useful sentence pairs for annotation. If pairs are chosen randomly from a text corpus, most of the pairs will have a very low similarity score while only few pairs will achieve a very high score. This can be circumvented if you automatically pre-select candidate pairs to have higher scores.

There are a few different methods for the pre-selection of candidate pairs but each of them come with their own issues. Word overlap based method like n-gram matching or the use of BM-25 (through elasticsearch) lead to candidate pairs which have high word overlap while similar pairs with low word overlap might not be found. Sentence embedding based methods such as semantic search with Sentence Transformers might be able to capture similarity with lower word overlap but candidate pairs are still limited to sentences which the model already knows to be similar. A combination of lexical and semantic approaches to candidate pair matching will probably lead to the most balanced set of candidate pairs.

In dualtext, the matching of one document to another document is left to the annotator and can be done dynamically. The annotator is presented with a single document and their task is to find a similar (or dissimilar) document from the provided text corpus. They can use a search bar in the application to search the text corpus and they can choose between different search methods to perform a search. Out of the box, dualtext provides BM-25 based search through elasticsearch and semantic search using a Sentence-BERT model. Search methods are extensible and additional search methods can easily be implemented.

Performing the search for matching documents dynamically allows for a diverse set of tasks which can lead to very high-quality and challenging textual similarity datasets. Using different search methods and providing different instructions to annotators will lead to datasets which are well balanced and capture different notions of textual similarity.

Here are some example instruction sets for annotators:


Finding similar sentences:

- Using elasticsearch, paste the sentence you are presented with in the search box, perform a search and pick the most similar sentence from the result list. Then assign a label from 0 to 5 depending on the similarity between those two sentences.
- Do the same as above but use semantic search instead
- You are presented with a sentence. Try to reformulate the sentence so that it has the same meaning but little word overlap. Paste the reformulated sentence in the search box, perform a search and pick the result that is most similar to the original sentence. Now assign a label from 0 to 5 depending on the similarity between those two sentences.

Finding hard negatives:

- Using semantic search, paste the sentence you are presented with in the search box, perform a search and pick a sentence from the result list which is highly ranked but you think that it actually has very low similarity to the original sentence. Now assign a label from 0 to 5 depending on the similarity between those two sentences.
- Using elasticsearch, try different search queries based on the sentence you are presented with. Try to formulate the search queries in a way that the results will have high word overlap with the original sentence but relatively low similarity. Try to find a sentence which you think would be difficult to identify as a dissimilar sentence. If you are happy with a sentence, pick the sentence from the result list. Now assign a label from 0 to 5 depending on the similarity between those two sentences.


