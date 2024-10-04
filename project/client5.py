import requests

URL = 'http://127.0.0.1:8000/api/v1/users/login'

USER = {
    'username': 'wbivanco',
    'password': 'wbivanco123'
}

response = requests.post(URL, json=USER)

if response.status_code == 200:
    print('Usuario autenticado de forma exitosa!')

    print(response.json()) 

    print(response.cookies) # RequestsCookieJar

    print(response.cookies.get_dict())