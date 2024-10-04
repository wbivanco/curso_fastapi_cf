import requests

REVIEW_ID = 2
URL = f'http://127.0.0.1:8000/api/v1/reviews/{REVIEW_ID}'

response = requests.delete(URL)

if response.status_code == 200:
    print('La reseña se eliminó en forma exitosa!')

    print(response.json()) 