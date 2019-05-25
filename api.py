import json

import requests


def _url(path):
    return f'http://localhost:8081{path}'


def get_usermessage(username):
    return requests.get(_url(f'/hello/{username}'))


def put_user(username, birthdate):
    user = {"dateOfBirth": birthdate}
    return requests.put(_url(f'/hello/{username}'), json=user)
