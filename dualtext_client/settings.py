import os
import json
from pathlib import Path

import click


USER_HOME = str(Path.home())

CONFIG_DIR = os.path.join(USER_HOME, '.dualtext')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config')

def set_config(**kwargs):
    if not os.path.isdir(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
    if not os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            f.write(json.dumps({}))

    with open(CONFIG_FILE, 'r') as f:
        config = json.loads(f.read())


    with open(CONFIG_FILE, 'w') as f:
        config = {**config, **kwargs}
        print(config)
        f.write(json.dumps(config))


def get_config():
    if os.path.isdir(CONFIG_DIR) and os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = f.read()
    else:
        config = json.dumps({})

    return config


API_URL = None

if os.path.isdir(CONFIG_DIR) and os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        try:
            config = json.loads(f.read())
            API_URL = config.get('API_URL', None)
            API_URL = API_URL + '/api/v1' if API_URL else None
        except json.JSONDecodeError:
            click.echo(f'Your config at {CONFIG_FILE} is not a valid configuration file. Try to remove the file and set up the configuration again. \n', err=True)



