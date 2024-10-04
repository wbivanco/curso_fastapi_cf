import requests

REVIEW_ID = 2
URL = f'http://127.0.0.1:8000/api/v1/reviews/{REVIEW_ID}'

REVIEW = {  
    'review': 'Excelente película',
    'score': 5
}

response = requests.put(URL, json=REVIEW)

if response.status_code == 200:
    print('La reseña se actulizó en forma exitosa!')

    print(response.json()) 