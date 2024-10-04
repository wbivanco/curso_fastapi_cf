import requests

URL = 'http://127.0.0.1:8000/api/v1/reviews'
REVIEW = {
    'user_id': 1,
    'movie_id': 1,
    'review': 'Excelente película',
    'score': 5
    }

response = requests.post(URL, json=REVIEW)

if response.status_code == 200:
    print('Reseña creada en forma exitosa!')
else:
    print(response.content) 