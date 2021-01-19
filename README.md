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
$ cd dualtext_server
$ pip install -r requirements.txt
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
$ pip install -r requirements.txt
$ pip install --editable
$ dualtext
```
You can now use the CLI.




