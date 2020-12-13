import requests
class Session():
    """
    docstring
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def login(self, username, password):
        response = self.session.post('http://localhost:8000/api/v1/login/', json={'username': username, 'password': password})
        token = response.json()['token']
        self.set_token(token)
        return token
    
    def set_token(self, token):
        self.session.headers.update({'Authorization': 'Token {}'.format(token)})
        return self.session
