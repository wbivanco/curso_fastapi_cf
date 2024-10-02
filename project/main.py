from fastapi import FastAPI

app = FastAPI(
    title='Proyecto para reseñar películas',
    description='En este proyecto seremos capaces de reseñar películas.',
    version='1'
)

@app.get('/')
async def index():
    return 'Hola mundo, desde un servidor en FastAPI'

@app.get('/about')
async def about():
    return 'About'