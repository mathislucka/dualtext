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
```


Create a virtual environment if you like.

Then:
```bash
$ cd dualtext_server
$ pip install -r requirements.txt
$ pyton




