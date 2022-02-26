import click
import sys
from corpus import Corpus
from cli_crud import list_resources, delete_resource


@click.group()
def corpus():
    pass


@corpus.command('ls')
@click.option(
    '--json',
    '-j',
    'json_output',
    is_flag=True,
    default=False
)
@click.option(
    "--out",
    help="File to write the output to, omit to display on screen.",
    type=click.File("w"),
    default=sys.stdout,
)
def list_corpora(json_output, out):
    list_resources(Corpus, json_output=json_output, out=out)


@corpus.command('delete')
@click.option(
    '--corpus-id',
    '-c',
    help='Id of corpus that you would like to delete.',
    type=click.INT,
    default=sys.stdin
)
@click.confirmation_option(prompt='Are you sure you want to delete the corpus?')
def delete_corpus(corpus_id):
    delete_resource(Corpus, entity_id=corpus_id)