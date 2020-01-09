import json
import random
import string
import requests


def randomString(stringLength=32):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def sendEmailWithLink(email, pendingHash):
    URL = 'https://script.google.com/macros/s/AKfycbxnPouS6ZQKy4XamVqbOe7YJ3cQ55oiM8c4GzB1ylF1ZYgqZWI/exec'
    r = requests.post(
        url=URL,
        data=json.dumps({'email': email, 'hash': pendingHash}),
        headers={'Content-Type': 'application/json'}
    )

    if r.status_code == 200:
        return True
    return False
