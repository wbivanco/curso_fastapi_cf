import requests

URL = 'http://127.0.0.1:8000/api/v1/reviews'
HEADERS = {'accept': 'application/json'}

response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    print('Petición realizada de forma exitosa!')

    if response.headers.get('content-type') == 'application/json':
        reviews = response.json()

        for review in reviews:
            print(f'> Score: {review["score"]}: {review["review"]}') 