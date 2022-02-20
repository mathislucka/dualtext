from settings import API_URL
import requests

class Session():
    """
    docstring
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.token = None
    
    def login(self, username, password):
        response = self.session.post(f'{API_URL}/login/', json={'username': username, 'password': password})
        token = response.json()['token']
        self.set_token(token)
        return self.session

    def validate_token(self):
        response = self.session.get(f'{API_URL}/validtoken/')

        return response.status_code == 200

    def set_token(self, token):
        self.session.headers.update({'Authorization': 'Token {}'.format(token)})
        self.token = token
        return self.session

    def get_token(self):
        return self.token
