import click
import keyring
from session import Session
from settings import API_URL

def authenticate():
    access_token = keyring.get_password('dualtext', 'token')
    if access_token:
        session = Session()
        session.set_token(access_token)
        token_valid = session.validate_token()
        session = session.session
        if not token_valid:
            click.echo('Invalid token found. Deleting token from keychain.', err=True)
            keyring.delete_password('dualtext', 'token')
            access_token = None

    if access_token is None:
        session = Session()
        username = click.prompt('Please enter your username')
        pw = click.prompt('Password', hide_input=True)
        click.echo(f'connecting to dualtext at {API_URL}', err=True)
        session = session.login(username, pw)
        click.echo('login successful', err=True)
        access_token = session.get_token()
        keyring.set_password('dualtext', 'token', access_token)

    return session