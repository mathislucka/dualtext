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
        response = self.session.post('http://localhost:8000/api/v1/login/', json={'username': username, 'password': password})
        token = response.json()['token']
        self.set_token(token)
        return self.session
    
    def set_token(self, token):
        self.session.headers.update({'Authorization': 'Token {}'.format(token)})
        self.token = token
        return self.session

    def get_token(self):
        return self.token
